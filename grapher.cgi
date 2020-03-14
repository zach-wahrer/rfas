#!/usr/bin/perl

# A graphing utility for the Routesetting Feedback Analysis Software
# Written by Zach Wahrer

### Load Modules ###.
use CGI qw(:standard);
use GD::Graph::Data;
use GD::Graph::lines;
use DateTime;
use DBI;

### Remove This debug line after finished with program ###
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

### Import config file vars ###
open CONFIG, "/usr/rfas/rfas_config.pl"
or die "Couldn't open the config file.";
my $config = join "", <CONFIG>;
close CONFIG;
eval $config;
die "Couldn't interpret the configuration file.\nError: $@\n" if $@;

### Connect to Database ###
$dbh = DBI->connect("dbi:mysql:route_feedback;host=$mysql_host", $mysql_username, $mysql_password)
or die "Connection Error: $DBI::errstr\n";

### Get Variables from HTML Line Input ###
$q = CGI->new();
$title = $q->param('title');
$amount = $q->param('amount');
$monthstart = $q->param('monthstart');
$duration = $q->param('duration');
$legend1 = $q->param('legend1');
$legend2 = $q->param('legend2');
$legend3 = $q->param('legend3');
$legend4 = $q->param('legend4');
$maxvalue = $q->param('maxvalue');
$ticks = $q->param('ticks');
$type = $q->param('type');
$setterid = $q->param('setterid');
$reviewdate = $q->param('reviewdate');

### Make the Months Array
($startmonth, $startyear) = split '/', $monthstart;
$formattedyear = substr $startyear, 2, 2;
$formattedstart = "$startmonth/$formattedyear";

if ($duration eq "sixmonths") {
	$time = "6";
}
elsif ($duration eq "oneyear") {
	$time = "12";
}
else { die "Incorrect input."; }

$dt = DateTime->new(
	year => $startyear,
	month => $startmonth
);

$startdate = "$startyear-$startmonth-01";

$counter = "0";
push (@months, "$formattedstart");
push (@reviewmonths, "$startyear-$startmonth-01");

while ($counter != $time) {
	$date = $dt->add( months => 1 );
	($year, $month, $everythingelse) = split '-', $date;
    $formattedyear = substr $year, 2, 2;
    $date = "$month/$formattedyear";
    push (@months, "$date");
    $datewithday = "$year-$month-01";
    push (@reviewmonths, "$datewithday");
    ++$counter;
  }

### Make the Boulder Grades Array
$sql = "SELECT `Boulder Grade` FROM `Boulder_Grade_Index`";
$sth = $dbh->prepare($sql);
$sth->execute
or die "SQL Error: $DBI::errstr\n";
## Put Results In an Array
while (@row = $sth->fetchrow_array) {
	push (@bouldergrades, @row);
}

### Make the Route Grades Array
$sql = "SELECT `Route Grade` FROM `Route_Grade_Index`";
$sth = $dbh->prepare($sql);
$sth->execute
or die "SQL Error: $DBI::errstr\n";
## Put Results In an Array
while (@row = $sth->fetchrow_array) {
	push (@routegrades, @row);
}

### Build Data Array
$quality = "`Soft1.Quality`, `Soft2.Quality`, `Soft3.Quality`, `Soft4.Quality`, `Soft5.Quality`, `Soft6.Quality`, `Soft7.Quality`, `Soft8.Quality`, `On1.Quality`, `On2.Quality`, `On3.Quality`, `On4.Quality`, `On5.Quality`, `On6.Quality`, `On7.Quality`, `On8.Quality`, `Hard1.Quality`, `Hard2.Quality`, `Hard3.Quality`, `Hard4.Quality`, `Hard5.Quality`, `Hard6.Quality`, `Hard7.Quality`, `Hard8.Quality`";


##### PRINT GRAPHS FOR EACH TYPE #####

#### Route Feedback Per Month
if ($type eq "dater") {
	foreach (@reviewmonths) {

		### SETTER ROUTES
		$sql = "SELECT $quality FROM `Feedback_Data` WHERE  (`Date` BETWEEN \"$_\" AND DATE_ADD(\"$_\", INTERVAL 1 MONTH) - INTERVAL 1 DAY) AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		## Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@routefeedback, @row);
		}

		### Average The Feedback
		foreach (@routefeedback) {
			if ($_ ne "" and $_ ne "x") {
				$feedbacktotal = $feedbacktotal + $_;
				++$totalcounter;
			}
		}
		if ($totalcounter) {
			$totalaverage = $feedbacktotal / $totalcounter;
		}

		## Round the Numbers
		$totalaverage = sprintf "%.2f", $totalaverage;
		push (@routes, $totalaverage);
		$feedbacktotal = "0";
		$totalcounter = "0";
		$totalaverage = "0";
		@routefeedback = ();

		### GYM AVERAGE ROUTES
		$sql = "SELECT $quality FROM `Feedback_Data` WHERE  (`Date` BETWEEN \"$_\" AND DATE_ADD(\"$_\", INTERVAL 1 MONTH) - INTERVAL 1 DAY) AND (`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		## Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@routefeedback, @row);
		}

		### Average The Feedback
		foreach (@routefeedback) {
			if ($_ ne "" and $_ ne "x") {
				$feedbacktotal = $feedbacktotal + $_;
				++$totalcounter;
			}
		}
		if ($totalcounter) {
			$totalaverage = $feedbacktotal / $totalcounter;
		}

		## Round the Numbers
		$totalaverage = sprintf "%.2f", $totalaverage;
		push (@groutes, $totalaverage);
		$feedbacktotal = "0";
		$totalcounter = "0";
		$totalaverage = "0";
		@routefeedback = ();
	}

	@data = (
		[ @months ],
		[ (@routes) ],
		[ (@groutes) ],
	);
}

## Boulder Feedback Per Month
elsif ($type eq	"dateb") {
	foreach (@reviewmonths) {

		### SETTER BOULDERS
		$sql = "SELECT $quality FROM `Feedback_Data` WHERE  (`Date` BETWEEN \"$_\" AND DATE_ADD(\"$_\", INTERVAL 1 MONTH) - INTERVAL 1 DAY) AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"B\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		##Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@routefeedback, @row);
		}

		### Average The Feedback
		foreach (@routefeedback) {
			if ($_ ne "" and $_ ne "x") {
				$feedbacktotal = $feedbacktotal + $_;
				++$totalcounter;
			}
		}
		if ($totalcounter) {
			$totalaverage = $feedbacktotal / $totalcounter;
		}

		##Round the Numbers
		$totalaverage = sprintf "%.2f", $totalaverage;
		push (@boulders, $totalaverage);
		$feedbacktotal = "0";
		$totalcounter = "0";
		$totalaverage = "0";
		@routefeedback = ();

		### GYM AVERAGE BOULDERS
		$sql = "SELECT $quality FROM `Feedback_Data` WHERE  (`Date` BETWEEN \"$_\" AND DATE_ADD(\"$_\", INTERVAL 1 MONTH) - INTERVAL 1 DAY) AND (`Type` = \"B\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		## Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@routefeedback, @row);
		}

		### Average The Feedback
		foreach (@routefeedback) {
			if ($_ ne "" and $_ ne "x") {
				$feedbacktotal = $feedbacktotal + $_;
				++$totalcounter;
			}
		}
		if ($totalcounter) {
			$totalaverage = $feedbacktotal / $totalcounter;
		}

		##Round the Numbers
		$totalaverage = sprintf "%.2f", $totalaverage;
		push (@gboulders, $totalaverage);
		$feedbacktotal = "0";
		$totalcounter = "0";
		$totalaverage = "0";
		@routefeedback = ();
	}

	@data = (
		[ @months ],
		[ (@boulders) ],
		[ (@gboulders) ],
	);
}

elsif ($type eq "boulderaveragebygrade") {

	#### Feedback Per Grade
	foreach (@bouldergrades) {
		## Clear Vars
		@routefeedback = ();
		@gradeid = ();

		### Get the grade ID for current grade
		$sql = "SELECT `ID` FROM `Boulder_Grade_Index` WHERE `Boulder Grade` = \"$_\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		##Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@gradeid, @row);
		}

		### Feedback FOR SETTER
		$sql = "SELECT $quality FROM `Feedback_Data` WHERE  (`Date` BETWEEN \"$startdate\" AND \"$reviewdate\") AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Grade` = \"$gradeid[0]\") AND(`Type` = \"B\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		## Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@routefeedback, @row);
		}

		### Average The Feedback
		foreach (@routefeedback) {
			if ($_ ne "" and $_ ne "x") {
				$feedbacktotal = $feedbacktotal + $_;
				++$totalcounter;
			}
		}
		if ($totalcounter) {
			$totalaverage = $feedbacktotal / $totalcounter;
		}

		##Round the Numbers
		$totalaverage = sprintf "%.2f", $totalaverage;
		push (@bouldersbymonth, $totalaverage);
		$feedbacktotal = "0";
		$totalcounter = "0";
		$totalaverage = "0";
		@routefeedback = ();

		### Feedback FOR GYM AVERAGE
		$sql = "SELECT $quality FROM `Feedback_Data` WHERE  (`Date` BETWEEN \"$startdate\" AND \"$reviewdate\") AND (`Grade` = \"$gradeid[0]\") AND(`Type` = \"B\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		##Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@routefeedback, @row);
		}

		### Average The Feedback
		foreach (@routefeedback) {
			if ($_ ne "" and $_ ne "x") {
				$feedbacktotal = $feedbacktotal + $_;
				++$totalcounter;
			}
		}
		if ($totalcounter) {
			$totalaverage = $feedbacktotal / $totalcounter;
		}

		##Round the Numbers
		$totalaverage = sprintf "%.2f", $totalaverage;
		push (@gabouldersbymonth, $totalaverage);
		$feedbacktotal = "0";
		$totalcounter = "0";
		$totalaverage = "0";
		@routefeedback = ();
	}

	@data = (
		[ @bouldergrades ],
		[ (@bouldersbymonth) ],
		[ (@gabouldersbymonth) ],
	);
}

elsif ($type eq "bouldernumberset") {

	foreach (@bouldergrades) {
		## Clear Vars
		@gradeid = ();
		@result = ();
		$counter = "0";

		### Get the grade ID for current grade
		$sql = "SELECT `ID` FROM `Boulder_Grade_Index` WHERE `Boulder Grade` = \"$_\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		##Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@gradeid, @row);
		}

		#### Get Total Number Set
		$sql = "SELECT `Date` FROM `Feedback_Data` WHERE  (`Date` BETWEEN \"$startdate\" AND \"$reviewdate\") AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Grade` = \"$gradeid[0]\") AND (`Type` = \"B\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		##Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@result, @row);
		}
		foreach (@result) {
			++$counter;
		}
		push (@bouldernumberset, "$counter");
	}

	@data = (
		[ @bouldergrades ],
		[ (@bouldernumberset) ],
	);
}

elsif ($type eq "routeaveragebygrade") {

	#### Feedback Per Grade
	foreach (@routegrades) {
		## Clear Vars
		@routefeedback = ();
		@gradeid = ();

		### Get the grade ID for current grade
		$sql = "SELECT `ID` FROM `Route_Grade_Index` WHERE `Route Grade` = \"$_\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		##Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@gradeid, @row);
		}

		###Feedback FOR SETTER
		$sql = "SELECT $quality FROM `Feedback_Data` WHERE  (`Date` BETWEEN \"$startdate\" AND \"$reviewdate\") AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Grade` = \"$gradeid[0]\") AND(`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		##Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@routefeedback, @row);
		}

		### Average The Feedback
		foreach (@routefeedback) {
			if ($_ ne "" and $_ ne "x") {
				$feedbacktotal = $feedbacktotal + $_;
				++$totalcounter;
			}
		}

		if ($totalcounter) {
			$totalaverage = $feedbacktotal / $totalcounter;
		}

		## Round the Numbers
		$totalaverage = sprintf "%.2f", $totalaverage;
		push (@routesbymonth, $totalaverage);
		$feedbacktotal = "0";
		$totalcounter = "0";
		$totalaverage = "0";
		@routefeedback = ();

		### Feedback FOR GYM AVERAGE
		$sql = "SELECT $quality FROM `Feedback_Data` WHERE  (`Date` BETWEEN \"$startdate\" AND \"$reviewdate\") AND (`Grade` = \"$gradeid[0]\") AND(`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		##Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@routefeedback, @row);
		}

		### Average The Feedback
		foreach (@routefeedback) {
			if ($_ ne "" and $_ ne "x") {
				$feedbacktotal = $feedbacktotal + $_;
				++$totalcounter;
			}
		}
		if ($totalcounter) {
			$totalaverage = $feedbacktotal / $totalcounter;
		}

		## Round the Numbers
		$totalaverage = sprintf "%.2f", $totalaverage;
		push (@garoutesbymonth, $totalaverage);
		$feedbacktotal = "0";
		$totalcounter = "0";
		$totalaverage = "0";
		@routefeedback = ();
	}

	@data = (
		[ @routegrades ],
		[ @routesbymonth ],
		[ @garoutesbymonth ],
	);
}

elsif ($type eq "routenumberset") {

	foreach (@routegrades) {
		## Clear Vars
		@gradeid = ();
		@result = ();
		$counter = "0";

		### Get the grade ID for current grade
		$sql = "SELECT `ID` FROM `Route_Grade_Index` WHERE `Route Grade` = \"$_\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		##Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@gradeid, @row);
		}

		#### Get Total Number Set
		$sql = "SELECT `Date` FROM `Feedback_Data` WHERE  (`Date` BETWEEN \"$startdate\" AND \"$reviewdate\") AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Grade` = \"$gradeid[0]\") AND (`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		##Put Results In an Array
		while (@row = $sth->fetchrow_array) {
			push (@result, @row);
		}
		foreach (@result) {
			++$counter;
		}
		push (@routenumberset, "$counter");
	}

	@data = (
		[ @routegrades ],
		[ @routenumberset ],
	);
}

else {
	die "You must enter a graph type.";
}

### Build the graph

my $graph = GD::Graph::lines->new(800, 500);
$graph->set(
			x_label => '',
			y_label => "$amount",
			title => "$title",
			y_max_value => $maxvalue,
			y_tick_number => $ticks,
			y_label_skip => 2,
		) or die $graph->error;
$graph->set_legend("$legend1", "$legend2", "$legend3", "$legend4");
my $format = $graph->export_format;
print header("image/$format");
binmode STDOUT;
print $graph->plot(\@data)->$format();
