#!/usr/bin/perl -w

# Routesetting Feedback Analysis Software v0.5
# Database setup tool
# Written by Zach Wahrer

use DBI;

### Import config file vars ###
open CONFIG, "/usr/rfas/rfas_config.pl" or die "Couldn't open the config file.";
my $config = join "", <CONFIG>;
close CONFIG;
eval $config;
die "Couldn't interpret the configuration file.\nError: $@\n" if $@;

### Connect to Database ###
$dbh = DBI->connect("dbi:mysql:;host=$mysql_host", $mysql_username, $mysql_password)
or die "Connection Error: $DBI::errstr\n";

$sql = "CREATE DATABASE route_feedback;";
$sth = $dbh->prepare($sql);
$sth->execute
or die "SQL Error: $DBI::errstr\n";

$sql = "USE route_feedback;";
$sth = $dbh->prepare($sql);
$sth->execute or die "SQL Error: $DBI::errstr\n";

open SQL_FILE, '<', "route_feedback.sql" or die "Couldn't open route_feedback.sql.";
    $sql_string = "";
    while (my $sql_line = <SQL_FILE>) {
        if ($sql_line eq "\n") {
            $sth = $dbh->prepare($sql_string);
            $sth->execute or die "SQL Error: $DBI::errstr\n";
            $sql_string = "";
        }
        else {
            $sql_string = $sql_string . $sql_line;
        }
    }
    if ($sql_string) {
        $sth = $dbh->prepare($sql_string);
        $sth->execute or die "SQL Error: $DBI::errstr\n";
        $sql_string = "";
    }
close SQL_FILE;

print "\nDatabase successfully configured.\n"
