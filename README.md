- To run this program and test if it works--

 -- we need to start up the virtual machine first. For this go to the vagrant directory.
 -- once inside, type the command vagrant up.
 -- the VM will start booting. Once this is done, type vagrant ssh.
 -- After this is done , you need to go to  the directory cd /vagrant/catalog (cd means change directory)
 -- First of all, you need to create the database schema.
 -- For this, run the python file database_setup.py using the command python database_setup.py
 -- Once the schema is created. You can run insert statements into tables running the python file lots_of_items.py
 -- Finally you can run the python file project.py
 -- Now you must open your browser and login to 'http://localhost:5000/'-- you will now be able to login to the application and do Create , Read, Update and Delete 
 	Operations
 -- You must have a Google- plus account to login to the application however.
 -- And create the credentials needed to access this application. For this you need to replace the already existing client-id 
    in the template login.html with your client-id, that Google will provide for you when you create a project in Google developers 
    site(developers.google.com) and ask for a client-id.