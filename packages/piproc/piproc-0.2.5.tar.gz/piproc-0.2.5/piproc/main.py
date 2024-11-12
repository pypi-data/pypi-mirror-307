import datetime
import os
import yaml
import boto3
import psycopg2
import sqlalchemy

from botocore.exceptions import NoCredentialsError
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import sessionmaker
from shapely.geometry import Polygon
from os.path import dirname as up

from .tables import Processing, Products, TestProcessing

class Piproc:
    '''
    Base class for piproc which handles all the communications between the Plastic-i
    modules and the processing database.
    '''
    def __init__(self, test=False):
        '''
        Initialise connection to the processing database, using locally found credentials or
        downloading them from s3.
        '''
        cred_path = os.path.join(up(up(__file__)), 'credentials.yml')

        if not os.path.isfile(cred_path):
            s3 = boto3.client('s3')
            s3.download_file('dockerfilecfg', 'credentials.yml', 
                os.path.join(up(up(__file__)), 'credentials.yml'))

        with open(cred_path, 'r') as f:
            self.cred = yaml.safe_load(f)

        db = sqlalchemy.create_engine('postgresql:///processing', 
            connect_args={'host': self.cred['processing_db']['host'],
                          'user': self.cred['processing_db']['user'],
                          'password': self.cred['processing_db']['password']})

        Session = sessionmaker(bind=db)
        self.session = Session()

        if test:
            self.proc_table = TestProcessing
        else:
            self.proc_table = Processing

    def notify(self, product_id, queue):
        '''
        Notify pimessage whem some processing has occurred to update the message queue if the
        process is running in production with a message queue and kubernetes.
        '''
        conn = psycopg2.connect(host=self.cred['processing_db']['host'], dbname='processing',
            user=self.cred['processing_db']['user'], password=self.cred['processing_db']['password'])

        cursor = conn.cursor()
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        message = str({"id": product_id}).replace("'", '"')
        cursor.execute(f"NOTIFY {queue}, '{message}'")

    def close(self):
        '''
        Close the database connection
        '''
        self.session.close()

    def check_planet_download(self, tile_dict, redownload, satellite=None):
        '''
        A function to check in the Plastic-i processing db if a Planet SuperDove scene has already
        been downloaded.
        '''
        product_id = tile_dict['id']

        tile_date = tile_dict['properties']['acquired']
        try:
            tile_date = datetime.datetime.strptime(tile_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            tile_date = datetime.datetime.strptime(tile_date, '%Y-%m-%dT%H:%M:%SZ')
        out_tile_date = datetime.datetime.strftime(tile_date, '%Y%m%d%H%M%S')

        # TODO: This needs to be checked it produces the correct output with clipped imagery
        bounds = Polygon(tile_dict['geometry']['coordinates'][0]).bounds
        lats = str([bounds[1], bounds[3]])
        lons = str([bounds[0], bounds[2]])

        # Check that file hasn't already been downloaded
        file = self.session.query(Processing).get(product_id)
        if file and not redownload:
            return True, None, None
        elif file and redownload:
            return False, product_id, out_tile_date
        else:
            cur_date = datetime.datetime.now()
            file = Processing(id=product_id, satellite=satellite, lons=lons, lats=lats, 
                              tile_date=tile_date, downloaded=0, date_searched=cur_date)
            self.session.add(file)
            self.session.commit()
            return False, product_id, out_tile_date

    def check_download(self, tile_dict, tilename, redownload):
        '''
        A function to check in the Plastic-i processing db if a tile has already been
        downloaded.
        '''
        cur_date = datetime.datetime.now()
        product_id = tile_dict.properties['s2:product_uri'].split('.SAFE')[0]

        # try:
        #     tilename = [i for i in product_id.split("_") if "T" in i and len(i) == 6][0][1:]
        # except IndexError as e:
        #     print(e)
        #     raise AttributeError('Old S2 tile format')

        #tile_date = tile_dict['properties']['datetime']
        crs = tile_dict.properties['proj:epsg']
        #tile_dt = datetime.datetime.strptime(tile_date, '%Y-%m-%dT%H:%M:%SZ')
        tile_dt = tile_dict.datetime
        out_tile_date = datetime.datetime.strftime(tile_dt, '%Y%m%d%H%M%S')

        bbox = tile_dict.bbox
        lats = str([bbox[1], bbox[3]])
        lons = str([bbox[0], bbox[2]])

        # Check that file hasn't already been downloaded
        file = self.session.query(self.proc_table).get(product_id)

        if file and not redownload:
            return True, None, None
        elif file and redownload:
            return False, product_id, out_tile_date
        else:
            file = self.proc_table(id=product_id, tile=tilename, lons=lons, 
                            lats=lats, tile_date=tile_dt, crs=crs,
                            prediction=0, date_searched=cur_date, satellite='sentinel2')
            self.session.add(file)
            self.session.commit()
            return False, product_id, out_tile_date
        
    def update_download(self, product_id, file_path, result=2, env=None):
        '''
        Update the processing db with the status of a sentinel-2 download
        '''

        file = self.session.query(Processing).get(product_id)

        # Update database with download path, download status and number of times downloaded
        file.downloaded = result
        if result == 2:
            # Only update number of times downloaded if download was successful
            try:
                file.no_downloaded += 1
            except TypeError:
                file.no_downloaded = 1
            file.download_path = file_path
            file.date_downloaded = datetime.datetime.now()
            file.indexed = 0

            if env == 'k8s':
                # Notify message queue that file has been downloaded when running with kubernetes.
                self.notify(product_id, 'pifind_download')
        self.session.commit()

    def check_indexing(self, satellite='sentinel2'):
        '''
        A function to check in the Plastic-i processing db if a tile has already been 
        indexed to the Plastic-i datacube.
        '''

        file = self.session.query(Processing).filter(Processing.downloaded == 2,
                Processing.indexed == 0, Processing.satellite == satellite).first()

        # Update row in db to indicate file is being processed
        file.indexed = -1
        self.session.commit()

        output = {'path': file.download_path,
                'dt': file.tile_date,
                'crs': file.crs,
                'id': file.id
                }
        return output

    def mq_index(self, product_id):
        '''
        A function to get data from the Plastic-i proccessing db for a tile when supplied an id.
        Used in production with a message queue and kubernetes.
        '''
        file = self.session.query(Processing).get(product_id)

        # Update row in db to indicate file is being processed
        file.indexed = -1
        self.session.commit()

        output = {'path': file.download_path,
                'dt': file.tile_date,
                'crs': file.crs,
                'id': file.id
                }
        return output

    def update_index(self, product_id, yaml_path, satellite='sentinel2', result=2, env=None, crs=None):
        '''
        Update the processing db with the status of a Sentinel-2 index process.
        '''

        file = self.session.query(Processing).get(product_id)

        if satellite == 'planet' or satellite == 'skysat':
            file.crs = crs # Add crs info to planet or skysat indexing

        file.indexed = result

        if result == 2:
            # Only update number of times downloaded if download was successful
            try:
                file.no_indexed += 1
            except TypeError:
                file.no_indexed = 1
            file.date_indexed = datetime.datetime.now()
            file.index_path = yaml_path
            file.prediction = 0
            
            if env == 'k8s' and satellite == 'sentinel2':
                # Notify message queue that file has been downloaded when running with kubernetes.
                self.notify(product_id, 'pifind_index')

        self.session.commit()

    def check_prediction(self, satellite='sentinel2'):
        '''
        A function to check in the Plastic-i processing db if a tile has already had
        a plastic prediction tile created from it.
        '''
        file = self.session.query(Processing).filter(Processing.indexed == 2,
            Processing.prediction == 0, Processing.satellite == satellite).first()

        if satellite == 'sentinel2':
            tile = file.tile
        elif satellite == 'planet' or satellite == 'skysat':
            tile = file.crs # Planet scenes don't have tiles so we use the crs to distinguish them
        
        output = {'x': file.lons,
                  'y': file.lats,
                  'date': file.tile_date,
                  'tile': tile,
                  'crs': file.crs,
                  'id': file.id
                }
        return output

    def mq_unet(self, product_id):
        '''
        A function to get data from the Plastic-i processing db for a tile supplied an id for running a unet.
        Used in production with a message queue and kubernetes.
        '''
        file = self.session.query(Processing).get(product_id)
        try:
            output = {'x': file.lons,
                    'y': file.lats,
                    'date': file.tile_date,
                    'tile': file.tile,
                    'crs': file.crs,
                    'id': file.id
                }
        except AttributeError:
            return None
        return output

    def update_unet(self, output, it, satellite='sentinel2', yaml_path=None, model=None, result=None, env=None):
        '''
        Update the product db with the status of an apply_unet process.
        '''
        file = self.session.query(Processing).get(output['id'])

        file.prediction = result
        file.pred_path = yaml_path
        file.model = model

        try:
            new_file = Products(id=f'{output["id"]}_{it}', base_id=output['id'], tile=file.tile,
                lons=str(output['lons']), lats=str(output['lats']), tile_date=file.tile_date,
                crs=file.crs, prediction=0, avg=float(output['avg']), min=float(output['min']),
                max=float(output['max']), std=float(output['std']), area=output['area'], 
                length=output['length'], geom='SRID=4326;'+str(output['geom']), satellite=satellite)
            self.session.add(new_file)
        except KeyError:
            # If no plastic files found, nothing to add to products db.
            pass

        # if env == 'k8s':
            # Notify message queue that file has been downloaded when running with kubernetes.
            # self.notify(f'{output["id"]}_{it}', 'pifind_prediction')

        self.session.commit()

    def check_xgboost(self, satellite='sentinel2'):
        '''
        A function to check in the Plastic-i processing db if a tile has already had
        a plastic prediction tile created from it.
        '''
        file = self.session.query(Products).filter(Products.prediction == 0, 
                                                   Products.satellite == satellite).first()
        if satellite == 'sentinel2':
            tile = file.tile
        elif satellite == 'planet' or satellite == 'skysat':
            tile = file.crs

        output = {
            'x': file.lons,
            'y': file.lats,
            'date': file.tile_date,
            'crs': file.crs,
            'id': file.id,
            'tile': tile,
            'geom': file.geom
        }
        output['geom'] = to_shape(output['geom'])
        return output

    def mq_xgboost(self, product_id):
        '''
        A function to get data from the Plastic-i processing db for a tile supplied an id for running xgboost.
        Used in production with a message queue and kubernetes.
        '''
        file = self.session.query(Products).get(product_id)
        output = {'x': file.lons,
                  'y': file.lats,
                  'date': file.tile_date,
                  'crs': file.crs,
                  'id': file.id,
                  'tile': file.tile,
                  'geom': file.geom
            }
        output['geom'] = to_shape(output['geom'])
        return output

    def update_xgboost(self, product_id, yaml_path, model, satellite='sentinel2', result=2, class_dict=None):
        '''
        Update the processing db with the status of an apply_models process.
        '''
        file = self.session.query(Products).get(product_id)
        
        file.prediction = result
        if result == 2:
            # Only update number of times downloaded if download was successful
            try:
                file.no_prediction += 1
            except TypeError:
                file.no_prediction = 1
            file.date_prediction = datetime.datetime.now()
            file.pred_path = yaml_path
            file.model = model

            if class_dict:
                # Convert from dictionary to str for upload to products db
                class_dict = str(class_dict)
                file.class_dict = class_dict
        self.session.commit()
