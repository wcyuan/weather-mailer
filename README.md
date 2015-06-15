# Weather Mailer

This is the code for weather-mailer.appspot.com.  

Started out by following the instructions at

  https://bradablog.appspot.com/?p=218

and cloning

  https://github.com/GoogleCloudPlatform/appengine-guestbook-python.

Then I followed https://github.com/fjakobs/cloud9-gae-template and ran

  curl https://raw.github.com/fjakobs/cloud9-gae-template/master/compile-gae.sh | bash

That didn't work, so, looking at https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python, I ran:

  cd ~/lib
  wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.22.zip 
  unzip google_appengine_1.9.22.zip
  rm google_appengine_1.9.22.zip
  cd
  mkdir bin
  cd bin
  ln -s ../lib/google_appengine/*.py .

Then, run the server with:

  $ dev_appserver.py --host $IP --port $PORT ~/workspace




  
  
