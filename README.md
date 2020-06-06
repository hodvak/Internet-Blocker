# Welcome to Box Internet Blocker.

**this project works only with Hot router(HOTBOX).**

What the program does is allow parents to turn off / turn on their children's internet from their computer

How to use the program:
1. Download the program from https://drive.google.com/file/d/1sy4VaacwPoecG8hZ3YFm9tUBJeciy6th/view?usp=sharing
2. Open in your computer http://192.168.1.1/
      1. Log in with 'admin' as username and password.
      2. Go To Password and change your password to something only you know.
3. go to your child's computer:
      1. press start and seaech and open cmd(Command prompt)
      2. On the cmd run this command:
         ```cmd
         ipconfig /all
         ```
      3. Search for the physical adress in 'Ethernet adapter'.
      
         Should look like this:
         ```cmd
         Physical Address......:12-34-56-78-9A-BC
         ```
4. Open the program on your computer.
      1. Go to 'Settings'.
            * Set username to 'admin' and password to your new password (what you changed at 2).
      2. Go to 'Add Device'.
            * Set the name
            * Set the mac as the pysical address(in 3 example its should be '12:34:56:78:9A:BC').
      3. Now you can disable/enable or choose time the program will disable/enable the child's internet(the program must be open for this to work).
      
