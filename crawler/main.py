import os
import requests
import shutil
import argparse
from get_data import get_data
import pandas as pd
import numpy as np

class urlfile:
	def __init__(self, filepath):
		self.filepath = filepath
	
	def load_data(self):
		#Participant Link and Substance Link are required only
		
		data = pd.read_csv(self.filepath, sep=';')
		links = np.stack((data['Substance Link'].values, data['Endpoint Link'].values), axis = 1)
		
		
		return links		


class AutoCrawler:
    def __init__(self, links, skip_already_exist=True, do_echa=True, download_path='download'):
        """
        :param skip_already_exist: Skips keyword already downloaded before. This is needed when re-downloading.
        :param do_google: Download from google.com (boolean)

        :param download_path: Download folder path
 
        """

        self.skip = skip_already_exist
 
        self.do_echa = do_echa

        self.download_path = download_path
        self.urls = links
 

        os.makedirs('./{}'.format(self.download_path), exist_ok=True)

    @staticmethod
    def all_dirs(path):
        paths = []
        for dir in os.listdir(path):
            if os.path.isdir(path + '/' + dir):
                paths.append(path + '/' + dir)

        return paths

    @staticmethod
    def all_files(path):
        paths = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.isfile(path + '/' + file):
                    paths.append(path + '/' + file)

        return paths

    @staticmethod
    def make_dir(dirname):
        current_path = os.getcwd()
        path = os.path.join(current_path, dirname)
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def save_object_to_file(object, file_path):
        try:
            with open('{}'.format(file_path), 'wb') as file:
                shutil.copyfileobj(object.raw, file)
        except Exception as e:
            print('Save failed - {}'.format(e))

    def download_images(self,data,folder_name):
        self.make_dir('{}'.format(folder_name))


        #no_ext_path = '{}/{}/{}_{}'.format(self.download_path, keyword, site_name, str(index).zfill(4))
        path = no_ext_path + '.' + ext
        self.save_object_to_file(response, path)


    def download_from_site(self, url):
    	
      try:
          collect = get_data()  # initialize chrome driver
      except Exception as e:
          print('Error occurred while initializing chromedriver - {}'.format(e))
          return

      try:
          print('Collecting data... from {}'.format(url))

          links = collect.echa(url)

          print('Downloading images from collected links... {} from {}'.format(keyword, site_name))
          self.download_images(keyword, links, site_name)

          print('Done {} : {}'.format(site_name, keyword))

      except Exception as e:
          print('Exception {}:{} - {}'.format(site_name, keyword, e))

    def download(self, args):
        self.download_from_site(url=args)

    def do_crawling(self):
        
        for (url_id , url) in enumerate(self.urls):
            dir_name = '{}/{}'.format(self.download_path, url_id)
            if os.path.exists(os.path.join(os.getcwd(), dir_name)) and self.skip:
                print('Skipping already existing directory {}'.format(dir_name))
                continue

            if self.do_echa:
            	#print(url)
            	self.download(url)
            break

        print('End Program')

    def imbalance_check(self):
        print('Data imbalance checking...')

        dict_num_files = {}

        for dir in self.all_dirs(self.download_path):
            n_files = len(self.all_files(dir))
            dict_num_files[dir] = n_files

        avg = 0
        for dir, n_files in dict_num_files.items():
            avg += n_files / len(dict_num_files)
            print('dir: {}, file_count: {}'.format(dir, n_files))

        dict_too_small = {}

        for dir, n_files in dict_num_files.items():
            if n_files < avg * 0.5:
                dict_too_small[dir] = n_files

        if len(dict_too_small) >= 1:
            for dir, n_files in dict_too_small.items():
                print('Data imbalance detected.')
                print('Below keywords have smaller than 50% of average file count.')
                print('I recommend you to remove these directories and re-download for that keyword.')
                print('_________________________________')
                print('Too small file count directories:')
                print('dir: {}, file_count: {}'.format(dir, n_files))

            print("Remove directories above? (y/n)")
            answer = input()

            if answer == 'y':
                # removing directories too small files
                print("Removing too small file count directories...")
                for dir, n_files in dict_too_small.items():
                    shutil.rmtree(dir)
                    print('Removed {}'.format(dir))

                print('Now re-run this program to re-download removed files. (with skip_already_exist=True)')
        else:
            print('Data imbalance not detected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip', type=str, default='true',
                        help='Skips keyword already downloaded before. This is needed when re-downloading.')
    parser.add_argument('--echa', type=str, default='true', help='Download from google.com (boolean)')
    #parser.add_argument('--f', type=str, help='file path to load')
  
    args = parser.parse_args()

    _skip = False if str(args.skip).lower() == 'false' else True
    _echa = False if str(args.echa).lower() == 'false' else True
    #_filepath = args.f
    
    print('Options - skip:{},  echa:{}'.format(_skip,  _echa))

    #crawler = AutoCrawler(skip_already_exist=_skip,  do_google=_google, do_naver=_naver, full_resolution=_full, face=_face)
    #crawler.do_crawling()
    data = urlfile('result_jz9h5wcg.csv')
    links = data.load_data()
    
    crawler = AutoCrawler(links, skip_already_exist=_skip,  do_echa=_echa)
    crawler.do_crawling()
    
    
