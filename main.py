'''
author: Pascal Nsunba
'''
from ui import app
import utils


if __name__ == "__main__":
  info = '''
  This program dispays reported crime data in South Africa
  during the period of 2005 to 2016
  '''
  print(info)
  
  app.run(utils_funcs = utils)

