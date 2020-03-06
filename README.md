# RFAS
---
RFAS (Routesetting Feedback Analysis Software) is a bit of code I wrote for CityROCK Climbing gym while I worked there as Assistant Director of Routesetting back in 2013/2014.

The purpose of RFAS is to allow routesetting teams to track and visualize customer provided feedback for performance reviews. It graphs data and gives a quantifiable look into how routesetters are doing, both as a individuals and a team. I successfully used this software to to help my fellow setters see where their strengths and weaknesses were.

I wanted to add more features to this program, but ended up leaving my position at the gym to pursue fiction writing full-time. If you can find a way to implement this script for your gym, feel free. I'd be happy to hear if it helps you. :-)


## Installing with Docker
---
The easiest way to get up and running with RFAS is to run it inside a Docker container.
1. In the `includes` directory, open `route_feedback.sql`. Scroll to the bottom, and add your routesetters under `Default`, using this format:
`INSERT INTO `Setter_Index` (`ID`, `Name`) VALUES
(1, 'Default'),
(2, 'Name 1'),
(3, 'Name 2');` etc. Make sure each entry is separated by a `,` and that the last line has a `;` instead. Note: If you ever need to remove a setter from RFAS, don't delete them from the `Setter_Index` table. Simply add a `#` before their name. Otherwise, it will break the program.
2. In the project's root directory, run `docker build -t rfas .` (Note that the ending `.` in the command is needed.) This will build a Docker container with Apache2 and configure RFAS to run inside it.
3. Still in the project's root directory, run `docker-compose up -d`. This will start RFAS as well as a separate MySQL server container.
4. Log in to your RFAS container, using `docker exec -it container-id bash`. Replace `container-id` with the id found from `docker ps`.
5. Exectue `./db-setup.pl` from within the container to set up the required MySQL database and tables.
6. In a web browser, navigate to `localhost:8080` and you should see the RFAS welcome screen!


## Development / Manual Install
---

### Prerequisites
For RFAS to run on your system, you'll need the following:
1. A web server capable of serving Perl CGI files. Apache2 works well out of the box.
2. A MySQL server with root access. See **Database Setup** below for more info on database configuration.
3. The following Perl modules installed on your server:
    * CGI
    * DateTime
    * DBD-mysql
    * DBI
    * GD-graph

### Database Setup
1. Complete steps 1 and 2 under **Installing** below.
2. In the `includes` directory, open `route_feedback.sql`. Scroll to the bottom, and add your routesetters under `Default`, using this format:

```
INSERT INTO `Setter_Index` (`ID`, `Name`) VALUES
(1, 'Default'),
(2, 'Name 1'),
(3, 'Name 2');
```

Note: If you ever need to remove a setter from RFAS, don't delete them from the `Setter_Index` table. Simply add a `#` before their name. Otherwise, it will break the program.
3. Run `db-setup.pl` in the `includes` folder. This will create a `route_feedback` database in MySQL and create the required structure.
4. Continue with step 3 under **Installing**.

### Installing
1. Copy the `includes/rfas_config.pl` to a secure location on  your machine. Edit it and change the variables to reflect your MySQL username, password, and sever address.
2. Open `rfas.cgi`, `grapher.cgi`, and `includes/db-setup.pl` and edit lines 16, 17, and 10, repectively, `open CONFIG, "/usr/config/rfas_config.pl"`, to point to your config you copied in the previous step.
3. Now, copy `rfas.cgi` and `grapher.cgi` into your web server's `cgi-bin`. Make sure the file permissions are set to allow execution of the files.
4. DO NOT leave `rfas.cgi` or `grapher.cgi` without some type of password protection (utilizing a `.htaccess` file is the easiest). The program was never intended to be run on a publicly available web sever, and some of the design decisions reflect that, ie. no access control.
5. Navigate to your web server via a browser and open `rfas.cgi`. If you did everything correctly, you should see "What would you like to do?"

### Built With
---
* Perl - The controller / web framework
* MySQL - The database
* GD::Graph Perl module - The graphing tool

## Author
---
**Zach Wahrer** - [zachtheclimber](https://github.com/zachtheclimber)

## License
---
RFAS is licensed under the GNU General Public License. Check out the [LICENSE](LICENSE) for more details.
