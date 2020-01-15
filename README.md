# RFAS
---
RFAS (Routesetting Feedback Analysis Software) is a bit of code I wrote for CityROCK Climbing gym while I worked there as Assistant Director of Routesetting back in 2013/2014.

The purpose of RFAS is to allow routesetting teams to track and visualize customer provided feedback for performance reviews. It graphs data and gives a quantifiable look into how routesetters are doing, both as a individuals and a team. I successfully used this software to to help my fellow setters see where their strengths and weaknesses were.

I wanted to add more features to this program, but ended up leaving my position at the gym to pursue fiction writing full-time. If you can find a way to implement this script for your gym, feel free. I'd be happy to hear if it helps you. :-)

### Prerequisites
---
For RFAS to run on your system, you'll need the following:
1. A web server capable of serving Perl CGI files. Apache2 works well out of the box.
2. A MySQL server with a database called `route_feeback`. See **Database Setup** below for more info on database configuration.
3. The following Perl modules installed on your server:
    * CGI
    * DateTime
    * DBD-mysql
    * DBI
    * GD-graph

### Database Setup
---
Likely, the easiest way to set up a RFAS database is to use `phpmyadmin`. YMMV.

1. Import the `route_feedback.sql` file into your MySQL server (using `phpmyadmin`, if you choose), and this will set up the structure you need.
2. Manually insert your setters' names into the `Setter_Index` table. You should only have to do a name, as the `ID` will auto-increment. If you ever need to remove a setter, don't delete them from the table. Simply add a `#` before their name.

### Installing
---
1. Copy the `rfas.cgi` and `grapher.cgi` files into your web server's `cgi-bin`. Make sure the file permissions are set to allow execution of the files.
2. Copy the `includes` directory into the `cgi-bin`. Rename `includes/rfas_config.sample.pl` to `includes/rfas.config.pl`.
3. Edit `includes/rfas_config.pl` and change the variables to reflect your MySQL username / password.
4. Make sure your web server permissions will not allow someone to open the config file and see your password.
5. DO NOT leave `rfas.cgi` without some type of password protection (utilizing a `.htaccess` file is the easiest). The program was never intended to be run on a publicly available web sever, and some of the design decisions reflect that.
6. Navigate to your web server via a browser and open `rfas.cgi`. If you did everything correctly, you should see "What would you like to do?"

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
