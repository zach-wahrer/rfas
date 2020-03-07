#!/usr/bin/perl -w

# Routesetting Feedback Analysis Software v0.5
# Written by Zach Wahrer

### Load Modules ###
use CGI qw(:standard);
use DBI;
use Scalar::Util qw(looks_like_number);
use DateTime;

### Remove This debug line after finished with program ###
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

### Import config file vars ###
open CONFIG, "/usr/config/rfas_config.pl"
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
$action = $q->param('action');

### Load Calendar widget if Action is present ###
if (defined($action)) {
	$calendarwidget = '<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
		<script src="http://code.jquery.com/jquery-1.9.1.js"></script>
		<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
		<link rel="stylesheet" href="/resources/demos/style.css" />
		<script>
		$(function() {
		$( "#datepicker" ).datepicker();
		});
		$(function() {
		$( "#datepicker1" ).datepicker1();
		});
		</script>'
};

## Start HTML
print "Content-type:  text/html\n\n";
print "<head>\n";
print "<title>RFAS - V0.5</title>\n";
print $calendarwidget;
print "</head>\n";
print "<body>\n";

### Print Title
print "Routesetting Feedback Analysis System, V0.5. <br><br><br>\n";

########### Print User Options if first run ########

if ($action eq "") {
	print "What would you like to do?\n<p>\n
		<a href=\"rfas.cgi?action=add\"/>Add Feedback</a><br>\n
		<a href=\"rfas.cgi?action=print\"/>Print Report</a><br>\n
		<a href=\"rfas.cgi?action=team\"/>Team Report</a><br>\n";
}

########### Run Add Feedback if Selected ##########

elsif ($action eq "add") {

	### Start Form for Adding Feedback
	print "<form action=\"rfas.cgi\" name=\"AddFeedbackForm\" method=\"GET\">\n";

	### Print Setter Name Boxes ###
	$sql = "SELECT `Name` FROM `Setter_Index`";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";
	## Put Results In an Array
	while (@row = $sth->fetchrow_array) {
		push (@setternames, @row);
	}
	## Print Boxes
	print "Setter: \n";

	## Print Combo Box1
	print "<select name=\"setter1\">\n
			<option value=\"Blank\"> </option>\n";
	foreach (@setternames) {
		## Don't print if setter is inactive
		$oldsetter = m\#\;
		if (!$oldsetter) {
			print "<option value=\"$_\">$_</option>\n";
		}
	}
	print "</select>";

	## Print Combo Box2
	print "<select name=\"setter2\">
			<option value=\"Blank\"> </option>\n";
	foreach (@setternames) {
		$oldsetter = m\#\;
		if (!$oldsetter) {
			print "<option value=\"$_\">$_</option>\n";
		}
	}
	print "</select>";

	##Print Combo Box3
	print "<select name=\"setter3\">\n
			<option value=\"Blank\"> </option>\n";
	foreach (@setternames) {
		$oldsetter = m\#\;
		if (!$oldsetter) {
			print "<option value=\"$_\">$_</option>\n";
		}
	}
	print "</select>\n";

	### Date Box
	print '<br><br><br>Date: <input type="text" name=date id="datepicker" /></p>';


	### Print Route Rating Boxes
	$sql = "SELECT `Route Grade` FROM `Route_Grade_Index`";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";
	##Put Results In an Array
	while (@row = $sth->fetchrow_array) {
		push (@routegrade, @row);
	}

	##Print Grade Box
	print "<br><br>Route Rating: \n";
	print "<select name=\"routegrade\">\n
			<option value=\"Blank\"> </option>\n";
	foreach (@routegrade) {
		print "<option value=\"$_\">$_</option>\n";
	}
	print "</select>";

	##  Print Original Grade Box
	print "<p>Orignal Route Rating:\n";
	print "<select name=\"routeoriginalgrade\">\n
			<option value=\"Blank\"> </option>\n";
	foreach (@routegrade) {
		print "<option value=\"$_\">$_</option>\n";
	}
	print "</select>\n\n";


	###Print Boulder Rating Boxes
	$sql = "SELECT `Boulder Grade` FROM `Boulder_Grade_Index`";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";
	while (@row = $sth->fetchrow_array) {
		push (@bouldergrade, @row);
	}

	##Print Grade Box
	print "<br><br><br>Boulder Rating: \n";
	print "<select name=\"bouldergrade\">\n
			<option value=\"Blank\"> </option>\n";
	foreach (@bouldergrade) {
		print "<option value=\"$_\">$_</option>\n";
	}
	print "</select>";

	##  Print Original Grade Box
	print "<p>Orignal Boulder Rating:\n";
	print "<select name=\"boulderoriginalgrade\">\n
			<option value=\"Blank\"> </option>\n";
	foreach (@bouldergrade) {
		print "<option value=\"$_\">$_</option>\n";
	}
	print "</select>\n\n";


	###Feedback Matrix
	print "<br><br><br>Feedback:<p>\n";
	### Soft Feedback
	print "Soft: \n";
	print '<input type="text" maxlength="3" size="2" name="Soft1">';
	print '<input type="text" maxlength="3" size="2" name="Soft2">';
	print '<input type="text" maxlength="3" size="2" name="Soft3">';
	print '<input type="text" maxlength="3" size="2" name="Soft4">';
	print '<input type="text" maxlength="3" size="2" name="Soft5">';
	print '<input type="text" maxlength="3" size="2" name="Soft6">';
	print '<input type="text" maxlength="3" size="2" name="Soft7">';
	print '<input type="text" maxlength="3" size="2" name="Soft8">';

	### On Grade Feedback
	print "<p>On: \n";
	print '<input type="text" maxlength="3" size="2" name="On1">';
	print '<input type="text" maxlength="3" size="2" name="On2">';
	print '<input type="text" maxlength="3" size="2" name="On3">';
	print '<input type="text" maxlength="3" size="2" name="On4">';
	print '<input type="text" maxlength="3" size="2" name="On5">';
	print '<input type="text" maxlength="3" size="2" name="On6">';
	print '<input type="text" maxlength="3" size="2" name="On7">';
	print '<input type="text" maxlength="3" size="2" name="On8">';

	### Hard Feedback
	print "<p>Hard: \n";
	print '<input type="text" maxlength="3" size="2" name="Hard1">';
	print '<input type="text" maxlength="3" size="2" name="Hard2">';
	print '<input type="text" maxlength="3" size="2" name="Hard3">';
	print '<input type="text" maxlength="3" size="2" name="Hard4">';
	print '<input type="text" maxlength="3" size="2" name="Hard5">';
	print '<input type="text" maxlength="3" size="2" name="Hard6">';
	print '<input type="text" maxlength="3" size="2" name="Hard7">';
	print '<input type="text" maxlength="3" size="2" name="Hard8">';

	#### Comment Boxes
	print '<br><br>Comment 1: <input type="text" maxlength="100" size="50" name="Comment1"><br>';
	print 'Comment 2: <input type="text" maxlength="100" size="50" name="Comment2"><br>';
	print 'Comment 3: <input type="text" maxlength="100" size="50" name="Comment3"><br>';
	print 'Comment 4: <input type="text" maxlength="100" size="50" name="Comment4"><br>';
	print 'Comment 5: <input type="text" maxlength="100" size="50" name="Comment5"><br>';
	print 'Comment 6: <input type="text" maxlength="100" size="50" name="Comment6"><br>';
	print 'Comment 7: <input type="text" maxlength="100" size="50" name="Comment7"><br>';
	print 'Comment 8: <input type="text" maxlength="100" size="50" name="Comment8"><br>';

	###Make submit/reset buttons and finish form
	print "<br><br><br>";
	print submit ('action', 'Submit');
	print reset;
	print "</form>";

}


############# Add to Database if Data is Submitted ###############

elsif ($action eq "Submit") {

	### Get Variables
	$setter1 = $q->param('setter1');
	$setter2 = $q->param('setter2');
	$setter3 = $q->param('setter3');
	$date = $q->param('date');
	$routegrade = $q->param('routegrade');
	$routeoriginalgrade = $q->param('routeoriginalgrade');
	$bouldergrade = $q->param('bouldergrade');
	$boulderoriginalgrade = $q->param('boulderoriginalgrade');
	$Soft1 = $q->param('Soft1');
	$Soft2 = $q->param('Soft2');
	$Soft3 = $q->param('Soft3');
	$Soft4 = $q->param('Soft4');
	$Soft5 = $q->param('Soft5');
	$Soft6 = $q->param('Soft6');
	$Soft7 = $q->param('Soft7');
	$Soft8 = $q->param('Soft8');
	$On1 =  $q->param('On1');
	$On2 = $q->param('On2');
	$On3 = $q->param('On3');
	$On4 = $q->param('On4');
	$On5 = $q->param('On5');
	$On6 = $q->param('On6');
	$On7 = $q->param('On7');
	$On8 = $q->param('On8');
	$Hard1 = $q->param('Hard1');
	$Hard2 = $q->param('Hard2');
	$Hard3 = $q->param('Hard3');
	$Hard4 = $q->param('Hard4');
	$Hard5 = $q->param('Hard5');
	$Hard6 = $q->param('Hard6');
	$Hard7 = $q->param('Hard7');
	$Hard8 = $q->param('Hard8');
	$Comment1 = $q->param('Comment1');
	$Comment2 = $q->param('Comment2');
	$Comment3 = $q->param('Comment3');
	$Comment4 = $q->param('Comment4');
	$Comment5 = $q->param('Comment5');
	$Comment6 = $q->param('Comment6');
	$Comment7 = $q->param('Comment7');
	$Comment8 = $q->param('Comment8');

	@soft_on_hard = ($Soft1, $Soft2, $Soft3, $Soft4, $Soft5, $Soft6, $Soft7, $Soft8,
					$On1, $On2, $On3, $On4, $On5, $On6, $On7, $On8,
					$Hard1, $Hard2, $Hard3, $Hard4, $Hard5, $Hard6, $Hard7, $Hard8);

	### Get IDs for Variables ###
	#### Setter Names ####
	if ($setter1 eq "Blank") {
		die "You have to enter a First Setter!";
	}
	else {
		$sql = "SELECT `ID` FROM `Setter_Index` WHERE `Name` = \"$setter1\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		$setter1 = $sth->fetchrow_array;

		## Get IDs if 2nd Setter Exist and if not, make null
		if ($setter2 ne "Blank") {
			$sql = "SELECT `ID` FROM `Setter_Index` WHERE `Name` = \"$setter2\"";
			$sth = $dbh->prepare($sql);
			$sth->execute
			or die "SQL Error: $DBI::errstr\n";

			$setter2 = $sth->fetchrow_array;
		}
		else {
			$setter2 = undef;
		}

		## Get IDs if 3rd Setters Exist	and if not, make null
		if ($setter3 ne "Blank") {
			$sql = "SELECT `ID` FROM `Setter_Index` WHERE `Name` = \"$setter3\"";
			$sth = $dbh->prepare($sql);
			$sth->execute
			or die "SQL Error: $DBI::errstr\n";

			$setter3 = $sth->fetchrow_array;

		}
		else {
			$setter3 = undef;
		}
	}

	###### Date ######
	if ($date eq "") {
		die "You have to enter a date!";
	}
	### Reformat Date
	($month, $day, $year) = split(m[/], $date);
	$date = "$year-$month-$day";
	### Validate Date
	if (! looks_like_number $year or ! looks_like_number $month or ! looks_like_number $day or $month > "12" or $month < "01" or $day > "31" or $day < "01" or $year < "2000") {
		die "You have entered an incorrectly formated date."
	}

	###### Route / Boulder Grades ######
	if ($routegrade eq "Blank" and $routeoriginalgrade eq "Blank" and $bouldergrade eq "Blank" and $boulderoriginalgrade eq "Blank") {
		die "You have to enter a Grade!";
	}

	### Die if an original grade is entered without a grade
	if ($routeoriginalgrade ne "Blank" and $routegrade eq "Blank") {
		die "You have to enter a Route Grade with an Original Grade!";
	}

	if ($boulderoriginalgrade ne "Blank" and $bouldergrade eq "Blank") {
		die "You have to enter a Bouldering Grade with an Original Grade!";
	}

	### Die if route grade and boulder grade are entered
	if ($bouldergrade ne "Blank" and $routegrade ne "Blank") {
		die "You cannot enter both Bouldering and Route grades at the same time.";
	}

	### Look up route grade ID and original grade if route is selected
	if ($routegrade ne "Blank") {
		$sql = "SELECT `ID` FROM `Route_Grade_Index` WHERE `Route Grade` = \"$routegrade\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		$routegrade = $sth->fetchrow_array;

		## Set Type to Route and make grade variable
		$type = "R";
		$grade = $routegrade;
	}

	if ($routeoriginalgrade ne "Blank") {
		$sql = "SELECT `ID` FROM `Route_Grade_Index` WHERE `Route Grade` = \"$routeoriginalgrade\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		$routeoriginalgrade = $sth->fetchrow_array;

		##Set grade variable
		$originalgrade = $routeoriginalgrade;
	}

	### Look up boulder grade ID and original grade if boulder is selected
	if ($bouldergrade ne "Blank") {

		$sql = "SELECT `ID` FROM `Boulder_Grade_Index` WHERE `Boulder Grade` = \"$bouldergrade\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";
		$bouldergrade = $sth->fetchrow_array;

		## Set Type to Boulder and make grade variable
		$type = "B";
		$grade = $bouldergrade;
	}

	if ($boulderoriginalgrade ne "Blank") {
		$sql = "SELECT `ID` FROM `Boulder_Grade_Index` WHERE `Boulder Grade` = \"$boulderoriginalgrade\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";
		$boulderoriginalgrade = $sth->fetchrow_array;

		##Set grade variable
		$originalgrade = $boulderoriginalgrade;
	}

	### Make sure Soft/On/Hard + Quality ratings aren't <5 or less than 0 or a non-number ###
	foreach (@soft_on_hard) {
		if ($_ ne "x" and $_ ne "" and ! looks_like_number $_) {
			die "You entered an improperly formatted feedback score.";
		}
		elsif ($_ > "5" or $_ < "0") {
			die "You cannot enter a feedback score higher than 5 or less than 0."
		}
	}

	### Put Data Into Database ###
	$sql = "INSERT INTO `route_feedback`.`Feedback_Data` (`Index`, `Name1`, `Name2`, `Name3`, `Type`, `Grade`, `OriginalGrade`, `Date`, `Soft1.Quality`, `Soft2.Quality`, `Soft3.Quality`, `Soft4.Quality`, `Soft5.Quality`, `Soft6.Quality`, `Soft7.Quality`, `Soft8.Quality`, `On1.Quality`, `On2.Quality`, `On3.Quality`, `On4.Quality`, `On5.Quality`, `On6.Quality`, `On7.Quality`, `On8.Quality`, `Hard1.Quality`, `Hard2.Quality`, `Hard3.Quality`, `Hard4.Quality`, `Hard5.Quality`, `Hard6.Quality`, `Hard7.Quality`, `Hard8.Quality`, `Comment1`, `Comment2`, `Comment3`, `Comment4`, `Comment5`, `Comment6`, `Comment7`, `Comment8`)
		VALUES (NULL, '$setter1', '$setter2', '$setter3', '$type', '$grade', '$originalgrade', '$date', '$Soft1', '$Soft2', '$Soft3', '$Soft4', '$Soft5', '$Soft6', '$Soft7', '$Soft8', '$On1', '$On2', '$On3', '$On4', '$On5', '$On6', '$On7', '$On8', '$Hard1', '$Hard2', '$Hard3', '$Hard4', '$Hard5', '$Hard6', '$Hard7', '$Hard8', '$Comment1', '$Comment2', '$Comment3', '$Comment4', '$Comment5', '$Comment6', '$Comment7', '$Comment8');";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";

	print "Feedback successfully entered! <p>\n
			What would you like to do now?\n<p>\n
			<a href=\"rfas.cgi?action=add\"/>Add Feedback</a><br>\n
			<a href=\"rfas.cgi?action=print\"/>Print Report</a><br>\n
			<a href=\"rfas.cgi?action=team\"/>Team Report</a><br>\n";
}

############# Run Print Report if Selected ###############

elsif ($action eq "print") {

	print "Print Report<br><br>";
	print "<form action=\"rfas.cgi\" name=\"PrintReportForm\" method=\"GET\">\n";

	### Print Setter Name Box
	$sql = "SELECT `Name` FROM `Setter_Index`";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";
	while (@row = $sth->fetchrow_array) {
		push (@setternames, @row);
	}

	print "Setter: \n";

	## Print Combo Box1
	print "<select name=\"setter\">\n
			<option value=\"Blank\"> </option>\n";
	foreach (@setternames) {
		$oldsetter = m\#\;
		if (!$oldsetter) {
			print "<option value=\"$_\">$_</option>\n";
		}
	}
	print "</select>";

	### Date Boxes
	print '<br><br>Review Date: <input type="text" name=reviewdate id="datepicker" autocomplete="off"/><br><br>';

	### Print Available Date Range
	$sql = "SELECT Date FROM `Feedback_Data` ORDER BY Date DESC LIMIT 1;";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";
	$newest_date = $sth->fetchrow_array;

	$sql = "SELECT Date FROM `Feedback_Data` ORDER BY Date ASC LIMIT 1;";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";
	$oldest_date = $sth->fetchrow_array;

	print "Data available from <b>$oldest_date</b> to <b>$newest_date</b>.<br><br>";


	### Print 6 months or year
	print "Length of Review:<br>";
	print '<input type="radio" name="duration" value="sixmonths"> 6 Months<br>';
	print '<input type="radio" name="duration" value="oneyear"> 1 Year<br>';

	### Make submit/reset buttons and finish form
	print "<br><br><br>";
	print submit ('action', 'Report');
	print reset;
	print "</form>";

}


### Print Feedback Report if Setter is Selected
elsif ($action eq "Report") {

	### Get/Set Variables
	$setter = $q->param('setter');
	$reviewdate = $q->param('reviewdate');
	$duration = $q->param('duration');
	@softquality = ("Soft1.Quality", "Soft2.Quality", "Soft3.Quality", "Soft4.Quality", "Soft5.Quality", "Soft6.Quality", "Soft7.Quality", "Soft8.Quality");
	@onquality = ("On1.Quality", "On2.Quality", "On3.Quality", "On4.Quality", "On5.Quality", "On6.Quality", "On7.Quality", "On8.Quality");
	@hardquality = ("Hard1.Quality", "Hard2.Quality", "Hard3.Quality", "Hard4.Quality", "Hard5.Quality", "Hard6.Quality", "Hard7.Quality", "Hard8.Quality");

	### Check duration and set proper length of time
	if ($duration eq "sixmonths") {
		($month, $day, $year) = split '/', $reviewdate;
		$sixmonthsdate = DateTime->new( year => $year, month => $month, day => $day );
		$sixmonthsdate->subtract( months => 6 );
		($year, $month, $day) = split (m[-], $sixmonthsdate);
		$day = substr $day, 0, 2;
		$sixmonthsdate = "$month/$day/$year";
	}
	elsif ($duration eq "oneyear") {
		($month, $day, $year) = split '/', $reviewdate;
		$yeardate = DateTime->new( year => $year, month => $month, day => $day );
		$yeardate->subtract( months => 12 );
		($year, $month, $day) = split (m[-], $yeardate);
		$day = substr $day, 0, 2;
		$sixmonthsdate = "$month/$day/$year";
	}
	else {
		die "You must select a length of time."
	}

	##Get Setter ID
	$sql = "SELECT `ID` FROM `Setter_Index` WHERE `Name` = \"$setter\"";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";
	while (@row = $sth->fetchrow_array) {
		push (@ID, @row);
	}
	$setterid = $ID[0];

	### Start Page
	print "<b>$setter"; print "'s Feedback Scores<br>
			$sixmonthsdate - $reviewdate :</b><br><br>\n";

	### Reformat Dates
	($month, $day, $year) = split(m[/], $sixmonthsdate);
	$sixmonthsdate = "$year-$month-$day";
	($month, $day, $year) = split(m[/], $reviewdate);
	$reviewdate = "$year-$month-$day";

	############## COMBINED TOTALS #################

	### Soft Feedback Average ###

	### Put All Soft Feedback into An Array
	foreach (@softquality) {
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@softqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@softqualityratings, @row);
		}
		push (@softratings, @softqualityratings);

		## Get Gym Total Soft Feedback ##
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\'";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@gymsoftqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymsoftqualityratings, @row);
		}
		push (@gymsoftratings, @gymsoftqualityratings);
	}

	### Get Average for Soft Feedback
	foreach (@softratings) {
		if ($_ ne "" and $_ ne "x") {
			$softtotal = $softtotal + $_;
			++$softcounter;
		}
	}
	if ($softcounter) {
		$softaverage = $softtotal / $softcounter;
	}
	push (@totalaverage, @softratings);

	### Get Average for GYM Soft Feedback
	foreach (@gymsoftratings) {
		if ($_ ne "" and $_ ne "x") {
			$gymsofttotal = $gymsofttotal + $_;
			++$gymsoftcounter;
		}
	}
	if ($gymsoftcounter) {
		$gymsoftaverage = $gymsofttotal / $gymsoftcounter;
	}
	push (@gymtotalaverage, @gymsoftratings);


	### On Feedback Average ###

	### Put All On Feedback into An Array
	foreach (@onquality) {
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@onqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@onqualityratings, @row);
		}
		push (@onratings, @onqualityratings);
	}

	### Gym Wide On Feedback
	foreach (@onquality) {
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\'";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@gymonqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymonqualityratings, @row);
		}
		push (@gymonratings, @gymonqualityratings);
	}

	### Get Average for On Feedback
	foreach (@onratings) {
		if ($_ ne "" and $_ ne "x") {
			$ontotal = $ontotal + $_;
			++$oncounter;
		}
	}
	if ($oncounter) {
		$onaverage = $ontotal / $oncounter;
	}
	push (@totalaverage, @onratings);

	### Get GYM Average for On Feedback
	foreach (@gymonratings) {
		if ($_ ne "" and $_ ne "x") {
			$gymontotal = $gymontotal + $_;
			++$gymoncounter;
		}
	}
	if ($gymoncounter) {
		$gymonaverage = $gymontotal / $gymoncounter;
	}
	push (@gymtotalaverage, @gymonratings);


	### Hard Feedback Average ###

	### Put All Hard Feedback into An Array
	foreach (@hardquality) {
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@hardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@hardqualityratings, @row);
		}
			push (@hardratings, @hardqualityratings);
	}

	### GYM Hard Feedback
	foreach (@hardquality) {
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\'";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@gymhardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymhardqualityratings, @row);
		}
		push (@gymhardratings, @gymhardqualityratings);
	}

	### Get Average for Hard Feedback
	foreach (@hardratings) {
		if ($_ ne "" and $_ ne "x") {
			$hardtotal = $hardtotal + $_;
			++$hardcounter;
		}
	}
	if ($hardcounter) {
		$hardaverage = $hardtotal / $hardcounter;
	}
	push (@totalaverage, @hardratings);

	### Get Average for GYM HardFeedback
	foreach (@gymhardratings) {
		if ($_ ne "" and $_ ne "x") {
			$gymhardtotal = $gymhardtotal + $_;
			++$gymhardcounter;
		}
	}
	if ($gymhardcounter) {
		$gymhardaverage = $gymhardtotal / $gymhardcounter;
	}
	push (@gymtotalaverage, @gymhardratings);


	### Get Total Average for Feedback
	foreach (@totalaverage) {
		if ($_ ne "" and $_ ne "x") {
			$totaltotal = $totaltotal + $_;
			++$totalcounter;
		}
	}
	if ($totalcounter) {
		$totalaverage = $totaltotal / $totalcounter;
	}

	## Round the Numbers
	$softaveragefeedback = sprintf "%.2f", $softaverage;
	$onaveragefeedback = sprintf "%.2f", $onaverage;
	$hardaveragefeedback = sprintf "%.2f", $hardaverage;
	$totalaveragefeedback = sprintf "%.2f", $totalaverage;

	### Get Total Average for GYM Feedback
	foreach (@gymtotalaverage) {
		if ($_ ne "" and $_ ne "x") {
			$gymtotaltotal = $gymtotaltotal + $_;
			++$gymtotalcounter;
		}
	}
	if ($gymtotalcounter) {
		$gymtotalaverage = $gymtotaltotal / $gymtotalcounter;
	}

	##Round the Numbers
	$gymsoftaveragefeedback = sprintf "%.2f", $gymsoftaverage;
	$gymonaveragefeedback = sprintf "%.2f", $gymonaverage;
	$gymhardaveragefeedback = sprintf "%.2f", $gymhardaverage;
	$gymtotalaveragefeedback = sprintf "%.2f", $gymtotalaverage;


	################ BOULDER AVERAGES ################

	### Soft Feedback Average ###

	### Put All Soft Feedback into An Array
	foreach (@softquality) {
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"B\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@bouldersoftqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@bouldersoftqualityratings, @row);
		}
			push (@bouldersoftratings, @bouldersoftqualityratings);

		## GYM Feedback
			$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"B\")";
			$sth = $dbh->prepare($sql);
			$sth->execute
			or die "SQL Error: $DBI::errstr\n";
			#Zero Out Array for Each pass
			@gymbouldersoftqualityratings = ();
			while (@row = $sth->fetchrow_array) {
				push (@gymbouldersoftqualityratings, @row);
			}
			push (@gymbouldersoftratings, @gymbouldersoftqualityratings);
	}

	### Get Average for Soft Feedback
	foreach (@bouldersoftratings) {
		if ($_ ne "" and $_ ne "x") {
			$bouldersofttotal = $bouldersofttotal + $_;
			++$bouldersoftcounter;
		}
	}
	if ($bouldersoftcounter) {
		$bouldersoftaverage = $bouldersofttotal / $bouldersoftcounter;
	}
	push (@bouldertotalaverage, @bouldersoftratings);

	### Get Average for Soft Feedback
	foreach (@gymbouldersoftratings) {
		if ($_ ne "" and $_ ne "x") {
			$gymbouldersofttotal = $gymbouldersofttotal + $_;
			++$gymbouldersoftcounter;
		}
	}
	if ($gymbouldersoftcounter) {
		$gymbouldersoftaverage = $gymbouldersofttotal / $gymbouldersoftcounter;
	}
	push (@gymbouldertotalaverage, @gymbouldersoftratings);


	### On Feedback Average ###

	### Put All On Feedback into An Array
	foreach (@onquality) {
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"B\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@boulderonqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@boulderonqualityratings, @row);
		}
		push (@boulderonratings, @boulderonqualityratings);

		## GYM Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"B\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@gymboulderonqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymboulderonqualityratings, @row);
		}
		push (@gymboulderonratings, @gymboulderonqualityratings);
	}

	### Get Average for On Feedback
	foreach (@boulderonratings) {
		if ($_ ne "" and $_ ne "x") {
			$boulderontotal = $boulderontotal + $_;
			++$boulderoncounter;
		}
	}

	if ($boulderoncounter) {
		$boulderonaverage = $boulderontotal / $boulderoncounter;
	}
	push (@bouldertotalaverage, @boulderonratings);

	### Get GYM Average for On Feedback
	foreach (@gymboulderonratings) {
		if ($_ ne "" and $_ ne "x") {
			$gymboulderontotal = $gymboulderontotal + $_;
			++$gymboulderoncounter;
		}
	}

	if ($gymboulderoncounter) {
		$gymboulderonaverage = $gymboulderontotal / $gymboulderoncounter;

	}

	## Put On into Totals
	push (@gymbouldertotalaverage, @gymboulderonratings);


	### Hard Feedback Average ###

	### Put All Hard Feedback into An Array
	foreach (@hardquality) {
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"B\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@boulderhardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@boulderhardqualityratings, @row);
		}
			push (@boulderhardratings, @boulderhardqualityratings);

		## GYM Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"B\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";
		#Zero Out Array for Each pass
		@gymboulderhardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymboulderhardqualityratings, @row);
		}
		push (@gymboulderhardratings, @gymboulderhardqualityratings);
	}

	### Get Average for HardFeedback
	foreach (@boulderhardratings) {
		if ($_ ne "" and $_ ne "x") {
			$boulderhardtotal = $boulderhardtotal + $_;
			++$boulderhardcounter;
		}
	}
	if ($boulderhardcounter) {
		$boulderhardaverage = $boulderhardtotal / $boulderhardcounter;
	}
	push (@bouldertotalaverage, @boulderhardratings);

	### Get GYM Average for HardFeedback
	foreach (@gymboulderhardratings) {
		if ($_ ne "" and $_ ne "x") {
			$gymboulderhardtotal = $gymboulderhardtotal + $_;
			++$gymboulderhardcounter;
		}
	}

	if ($gymboulderhardcounter) {
		$gymboulderhardaverage = $gymboulderhardtotal / $gymboulderhardcounter;
	}
	push (@gymbouldertotalaverage, @gymboulderhardratings);

	### Get Total Average for Feedback
	foreach (@bouldertotalaverage) {
		if ($_ ne "" and $_ ne "x") {
			$bouldertotaltotal = $bouldertotaltotal + $_;
			++$bouldertotalcounter;
		}
	}
	if ($bouldertotalcounter) {
		$bouldertotalaverage = $bouldertotaltotal / $bouldertotalcounter;
	}

	##Round the Numbers
	$bouldersoftaveragefeedback = sprintf "%.2f", $bouldersoftaverage;
	$boulderonaveragefeedback = sprintf "%.2f", $boulderonaverage;
	$boulderhardaveragefeedback = sprintf "%.2f", $boulderhardaverage;
	$bouldertotalaveragefeedback = sprintf "%.2f", $bouldertotalaverage;

	### GYM Get Total Average for Feedback
	foreach (@gymbouldertotalaverage) {
		if ($_ ne "" and $_ ne "x") {
			$gymbouldertotaltotal = $gymbouldertotaltotal + $_;
			++$gymbouldertotalcounter;
		}
	}
	if ($gymbouldertotalcounter) {
		$gymbouldertotalaverage = $gymbouldertotaltotal / $gymbouldertotalcounter;
	}

	##Round the GYM Numbers
	$gymbouldersoftaveragefeedback = sprintf "%.2f", $gymbouldersoftaverage;
	$gymboulderonaveragefeedback = sprintf "%.2f", $gymboulderonaverage;
	$gymboulderhardaveragefeedback = sprintf "%.2f", $gymboulderhardaverage;
	$gymbouldertotalaveragefeedback = sprintf "%.2f", $gymbouldertotalaverage;


	################## ROUTE AVERAGES ###############

	### Soft Feedback Average ###

	### Put All Soft Feedback into An Array
	foreach (@softquality) {
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@routesoftqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@routesoftqualityratings, @row);
		}
		push (@routesoftratings, @routesoftqualityratings);

		## GYM Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@gymroutesoftqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymroutesoftqualityratings, @row);
		}
		push (@gymroutesoftratings, @gymroutesoftqualityratings);
	}

	### Get Average for Soft Feedback
	foreach (@routesoftratings) {
		if ($_ ne "" and $_ ne "x") {
			$routesofttotal = $routesofttotal + $_;
			++$routesoftcounter;
		}
	}
	if ($routesoftcounter) {
		$routesoftaverage = $routesofttotal / $routesoftcounter;
	}
	push (@routetotalaverage, @routesoftratings);

	### GYM Get Average for Soft Feedback
	foreach (@gymroutesoftratings) {
		if ($_ ne "" and $_ ne "x") {
			$gymroutesofttotal = $gymroutesofttotal + $_;
			++$gymroutesoftcounter;
		}
	}
	if ($gymroutesoftcounter) {
		$gymroutesoftaverage = $gymroutesofttotal / $gymroutesoftcounter;
	}
	push (@gymroutetotalaverage, @gymroutesoftratings);


	### On Feedback Average ###

	### Put All On Feedback into An Array
	foreach (@onquality) {
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@routeonqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@routeonqualityratings, @row);
		}
		push (@routeonratings, @routeonqualityratings);

		## GYM Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@gymrouteonqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymrouteonqualityratings, @row);
		}
			push (@gymrouteonratings, @gymrouteonqualityratings);
	}

	### Get Average for On Feedback
	foreach (@routeonratings) {
		if ($_ ne "" and $_ ne "x") {
			$routeontotal = $routeontotal + $_;
			++$routeoncounter;
		}
	}
	if ($routeoncounter) {
		$routeonaverage = $routeontotal / $routeoncounter;
	}
	push (@routetotalaverage, @routeonratings);

	### GYM Get Average for On Feedback
	foreach (@gymrouteonratings) {
		if ($_ ne "" and $_ ne "x") {
			$gymrouteontotal = $gymrouteontotal + $_;
			++$gymrouteoncounter;
		}
	}
	if ($gymrouteoncounter) {
		$gymrouteonaverage = $gymrouteontotal / $gymrouteoncounter;
	}
	push (@gymroutetotalaverage, @gymrouteonratings);


	### Hard Feedback Average ###

	### Put All Hard Feedback into An Array
	foreach (@hardquality) {
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@routehardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@routehardqualityratings, @row);
		}
		push (@routehardratings, @routehardqualityratings);

		## GYM Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		#Zero Out Array for Each pass
		@gymroutehardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymroutehardqualityratings, @row);
		}
		push (@gymroutehardratings, @gymroutehardqualityratings);
	}

	### Get Average for HardFeedback
	foreach (@routehardratings) {
		if ($_ ne "" and $_ ne "x") {
			$routehardtotal = $routehardtotal + $_;
			++$routehardcounter;
		}
	}
	if ($routehardcounter) {
		$routehardaverage = $routehardtotal / $routehardcounter;
	}
	push (@routetotalaverage, @routehardratings);

	### GYM Get Average for HardFeedback
	foreach (@gymroutehardratings) {
		if ($_ ne "" and $_ ne "x") {
			$gymroutehardtotal = $gymroutehardtotal + $_;
			++$gymroutehardcounter;
		}
	}
	if ($gymroutehardcounter) {
		$gymroutehardaverage = $gymroutehardtotal / $gymroutehardcounter;
	}
	push (@gymroutetotalaverage, @gymroutehardratings);

	### Get Total Average for Feedback
	foreach (@routetotalaverage) {
		if ($_ ne "" and $_ ne "x") {
			$routetotaltotal = $routetotaltotal + $_;
			++$routetotalcounter;
		}
	}

	if ($routetotalcounter) {
		$routetotalaverage = $routetotaltotal / $routetotalcounter;
	}

	##Round the Numbers
	$routesoftaveragefeedback = sprintf "%.2f", $routesoftaverage;
	$routeonaveragefeedback = sprintf "%.2f", $routeonaverage;
	$routehardaveragefeedback = sprintf "%.2f", $routehardaverage;
	$routetotalaveragefeedback = sprintf "%.2f", $routetotalaverage;

	### Get GYM Total Average for Feedback
	foreach (@gymroutetotalaverage) {
		if ($_ ne "" and $_ ne "x") {
			$gymroutetotaltotal = $gymroutetotaltotal + $_;
			++$gymroutetotalcounter;
		}
	}
	if ($gymroutetotalcounter) {
		$gymroutetotalaverage = $gymroutetotaltotal / $gymroutetotalcounter;
	}

	##Round the Numbers
	$gymroutesoftaveragefeedback = sprintf "%.2f", $gymroutesoftaverage;
	$gymrouteonaveragefeedback = sprintf "%.2f", $gymrouteonaverage;
	$gymroutehardaveragefeedback = sprintf "%.2f", $gymroutehardaverage;
	$gymroutetotalaveragefeedback = sprintf "%.2f", $gymroutetotalaverage;


	########## BOULDER % OF GRADE SET W/ FEEDBACK ###########

	@feedbackquality = (@softquality,@onquality,@hardquality);
	$sql = "SELECT  `ID` FROM  `Boulder_Grade_Index` ";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";

	while (@row = $sth->fetchrow_array) {
		push (@boulderindexgrades, @row);
	}

	### Get Number For Each Grade For Setter
	foreach (@boulderindexgrades) {

		### For Number Set Per Grade ###
		$sql = "SELECT `Index` FROM `Feedback_Data` WHERE `Grade` = \"$_\" AND`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"B\") ";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		$bouldernumberset = "0";
		while (@row = $sth->fetchrow_array) {
			++$bouldernumberset;
		}
		push (@bouldernumberset, $bouldernumberset);

		### For Total Set Per Grade ###
		$sql = "SELECT `Index` FROM `Feedback_Data` WHERE `Grade` = \"$_\" AND`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"B\") ";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		$bouldertotalnumberset = "0";
		while (@row = $sth->fetchrow_array) {
			++$bouldertotalnumberset;
		}
		push (@bouldertotalnumberset, $bouldertotalnumberset);

		### Make Grade Array ###
		$sql = "SELECT `Boulder Grade` FROM `Boulder_Grade_Index` WHERE `ID` = \"$_\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		while (@row = $sth->fetchrow_array) {
			push (@bouldergradeindex, @row);
		}

		### Get Feedback For Setter ###
		$grade = $_;
		@boulderfeedbackgrade = ();
		foreach (@feedbackquality) {
			$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Grade` = \"$grade\" AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"B\")";
			$sth = $dbh->prepare($sql);
			$sth->execute
			or die "SQL Error: $DBI::errstr\n";

			while (@row = $sth->fetchrow_array) {
				push (@boulderfeedbackgrade, @row);
			}
		}

		$setterfeedbacktotal = "0";
		$settertotalcounter = "0";
		$settertotalaverage = "0";

		### Average Setter Feedback
		foreach (@boulderfeedbackgrade) {
			if ($_ ne "" and $_ ne "x") {
				$setterfeedbacktotal = $setterfeedbacktotal + $_;
				++$settertotalcounter;
			}
		}
		if ($settertotalcounter) {
			$settertotalaverage = $setterfeedbacktotal / $settertotalcounter;
		}

		##Round the Numbers
		$settertotalaverage = sprintf "%.2f", $settertotalaverage;
		push (@settertotals, $settertotalaverage);

		### Get GYM Feedback Average ###
		$grade = $_;
		@boulderfeedbackgrade = ();
		foreach (@feedbackquality) {
			$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Grade` = \"$grade\" AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Type` = \"B\")";
			$sth = $dbh->prepare($sql);
			$sth->execute
			or die "SQL Error: $DBI::errstr\n";

			while (@row = $sth->fetchrow_array) {
				push (@boulderfeedbackgrade, @row);
			}

		}

		$gymfeedbacktotal = "0";
		$gymtotalcounter = "0";
		$gymtotalaverage = "0";

		### Average Setter Feedback
		foreach (@boulderfeedbackgrade) {
			if ($_ ne "" and $_ ne "x") {
				$gymfeedbacktotal = $gymfeedbacktotal + $_;
				++$gymtotalcounter;
			}
		}
		if ($gymtotalcounter) {
			$gymtotalaverage = $gymfeedbacktotal / $gymtotalcounter;
		}

		##Round the Numbers
		$gymtotalaverage = sprintf "%.2f", $gymtotalaverage;
		push (@gymtotals, $gymtotalaverage);

	}

	########## ROUTE % OF GRADE SET W/ FEEDBACK ###########

	## Query For Grades
	$sql = "SELECT  `ID` FROM  `Route_Grade_Index` ";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";

	while (@row = $sth->fetchrow_array) {
		push (@routeindexgrades, @row);
	}

	### Get Number For Each Grade For Setter
	foreach (@routeindexgrades) {

		### For Number Set Per Grade ###
		$sql = "SELECT `Index` FROM `Feedback_Data` WHERE `Grade` = \"$_\" AND`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"R\") ";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		$routenumberset = "0";

		while (@row = $sth->fetchrow_array) {
			++$routenumberset;
		}

		push (@routenumberset, $routenumberset);

		### For Total Set Per Grade ###
		$sql = "SELECT `Index` FROM `Feedback_Data` WHERE `Grade` = \"$_\" AND`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"R\") ";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		$routetotalnumberset = "0";

		while (@row = $sth->fetchrow_array) {
			++$routetotalnumberset;
		}
		push (@routetotalnumberset, $routetotalnumberset);

		### Make Grade Array ###
		$sql = "SELECT `Route Grade` FROM `Route_Grade_Index` WHERE `ID` = \"$_\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		while (@row = $sth->fetchrow_array) {
			push (@routegradeindex, @row);
		}

		### Get Feedback For Setter ###
		$grade = $_;
		@routefeedbackgrade = ();
		foreach (@feedbackquality) {
			## Query For Feedback
			$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Grade` = \"$grade\" AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"R\")";
			$sth = $dbh->prepare($sql);
			$sth->execute
			or die "SQL Error: $DBI::errstr\n";

			while (@row = $sth->fetchrow_array) {
				push (@routefeedbackgrade, @row);
			}
		}

		$setterfeedbacktotal = "0";
		$settertotalcounter = "0";
		$settertotalaverage = "0";

		### Average Setter Feedback
		foreach (@routefeedbackgrade) {
			if ($_ ne "" and $_ ne "x") {
				$setterfeedbacktotal = $setterfeedbacktotal + $_;
				++$settertotalcounter;
			}
		}
		if ($settertotalcounter) {
			$settertotalaverage = $setterfeedbacktotal / $settertotalcounter;
		}

		##Round the Numbers
		$settertotalaverage = sprintf "%.2f", $settertotalaverage;
		push (@routesettertotals, $settertotalaverage);


	### Get GYM Feedback Average ###
	$grade = $_;
	@routefeedbackgrade = ();
	foreach (@feedbackquality) {
		## Query For Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Grade` = \"$grade\" AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Type` = \"R\")";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		while (@row = $sth->fetchrow_array) {
			push (@routefeedbackgrade, @row);
		}
	}

	$gymfeedbacktotal = "0";
	$gymtotalcounter = "0";
	$gymtotalaverage = "0";

	### Average Setter Feedback
	foreach (@routefeedbackgrade) {
		if ($_ ne "" and $_ ne "x") {
			$gymfeedbacktotal = $gymfeedbacktotal + $_;
			++$gymtotalcounter;
		}
	}
	if ($gymtotalcounter) {
		$gymtotalaverage = $gymfeedbacktotal / $gymtotalcounter;
	}

	##Round the Numbers
	$gymtotalaverage = sprintf "%.2f", $gymtotalaverage;
		push (@routegymtotals, $gymtotalaverage);
	}


	########## GET COMMENTS #############

	$comments = "`Comment1`, `Comment2`, `Comment3`, `Comment4`, `Comment5`, `Comment6`, `Comment7`, `Comment8`";

	## BOULDERS

	## Query For Feedback
	$sql = "SELECT $comments FROM `Feedback_Data` WHERE (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Type` = \"B\")";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";

	while (@row = $sth->fetchrow_array) {
			$comment = "";
			if ($row[0] ne "") {
				$comment = $row[0];
			}
			if ($row[1] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1]" ;
			}
			if ($row[2] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2]" ;
			}
			if ($row[3] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2] <font color = red>/</font> $row[3]" ;
			}
			if ($row[4] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2] <font color = red>/</font> $row[3] <font color = red>/</font> $row[4]" ;
			}
			if ($row[5] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2] <font color = red>/</font> $row[3] <font color = red>/</font> $row[4] <font color = red>/</font> $row[5]" ;
			}
			if ($row[6] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2] <font color = red>/</font> $row[3] <font color = red>/</font> $row[4] <font color = red>/</font> $row[5] <font color = red>/</font> $row[6]" ;
			}
			if ($row[7] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2] <font color = red>/</font> $row[3] <font color = red>/</font> $row[4] <font color = red>/</font> $row[5] <font color = red>/</font> $row[6] <font color = red>/</font> $row[7]" ;
			}

			push (@bouldercomments, "$comment");
	}

	## ROUTES

	## Query For Feedback
	$sql = "SELECT $comments FROM `Feedback_Data` WHERE (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Type` = \"R\")";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";

	while (@row = $sth->fetchrow_array) {
			$comment = "";
			if ($row[0] ne "") {
				$comment = $row[0];
			}
			if ($row[1] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1]" ;
			}
			if ($row[2] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2]" ;
			}
			if ($row[3] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2] <font color = red>/</font> $row[3]" ;
			}
			if ($row[4] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2] <font color = red>/</font> $row[3] <font color = red>/</font> $row[4]" ;
			}
			if ($row[5] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2] <font color = red>/</font> $row[3] <font color = red>/</font> $row[4] <font color = red>/</font> $row[5]" ;
			}
			if ($row[6] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2] <font color = red>/</font> $row[3] <font color = red>/</font> $row[4] <font color = red>/</font> $row[5] <font color = red>/</font> $row[6]" ;
			}
			if ($row[7] ne "") {
				$comment = "$row[0] <font color = red>/</font> $row[1] <font color = red>/</font> $row[2] <font color = red>/</font> $row[3] <font color = red>/</font> $row[4] <font color = red>/</font> $row[5] <font color = red>/</font> $row[6] <font color = red>/</font> $row[7]" ;
			}

			push (@routecomments, "$comment");
	}


	########## PRINT FEEDBACK ############

	#Format the Dates For Graphs
	($year, $month, $day) = split (m[-], $sixmonthsdate);
	$monthstart = "$month/$year";

	#### Print Averaged Route Feedback by Month Graph
	$title = "Averaged%20Boulder%20Feedback%20by%20Month";
	$amount = "Feedback%20Score";
	$legend1 = "$setter";
	$legend2 = "GA%20Boulders";
	$legend3 = "";
	$legend4 = "";
	$maxvalue = "5";
	$ticks = "40";
	$type = "dateb";
	print '<table border="1" style="width:1100px">';
	print "<tr><td><b>Combined Averages:</b></td><td>S:</td><td>GA:</td><td rowspan=15 align=center><img src=grapher.cgi?title=$title&amount=$amount&monthstart=$monthstart&duration=$duration&legend1=$legend1&legend2=$legend2&legend3=$legend3&legend4=$legend4&maxvalue=$maxvalue&ticks=$ticks&type=$type&setterid=$setterid&reviewdate=$reviewdate>\n";

	#### Print Averaged Route Feedback by Month Graph
	$title = "Averaged%20Route%20Feedback%20by%20Month";
	$amount = "Feedback%20Score";
	$legend1 = "$setter";
	$legend2 = "GA%20Routes";
	$legend3 = "";
	$legend4 = "";
	$maxvalue = "5";
	$ticks = "40";
	$type = "dater";

	print "<img src=grapher.cgi?title=$title&amount=$amount&monthstart=$monthstart&duration=$duration&legend1=$legend1&legend2=$legend2&legend3=$legend3&legend4=$legend4&maxvalue=$maxvalue&ticks=$ticks&type=$type&setterid=$setterid&reviewdate=$reviewdate></td></tr>\n";
	print "<tr><td>Soft:</td><td><b>$softaveragefeedback</b></td><td>$gymsoftaveragefeedback</td></tr>\n";
	print "<tr><td>On:</td><td><b>$onaveragefeedback</b></td><td>$gymonaveragefeedback</td></tr>\n";
	print "<tr><td>Hard:</td><td><b>$hardaveragefeedback</b></b></td><td>$gymhardaveragefeedback </td></tr>\n";
	print "<tr><td>Total: </td><td><b>$totalaveragefeedback</b></b></td><td>$gymtotalaveragefeedback </td></tr>\n";

	print "<tr><td><b>Boulder Averages:</b></tr></td>\n";
	print "<tr><td>Soft:</td><td> <b>$bouldersoftaveragefeedback</b></b></td><td>$gymbouldersoftaveragefeedback</td></tr>\n";
	print "<tr><td>On:</td><td> <b>$boulderonaveragefeedback</b></b></td><td>$gymboulderonaveragefeedback </td></tr>\n";
	print "<tr><td>Hard:</td><td> <b>$boulderhardaveragefeedback</b></b></td><td>$gymboulderhardaveragefeedback </td></tr>\n";
	print "<tr><td>Total:</td><td> <b>$bouldertotalaveragefeedback</b></b></td><td>$gymbouldertotalaveragefeedback </td></tr>\n";

	print "<tr><td><b>Route Averages:</b></tr></td>\n";
	print "<tr><td>Soft:</td><td> <b>$routesoftaveragefeedback</b></b></td><td>$gymroutesoftaveragefeedback </td></tr>\n";
	print "<tr><td>On:</td><td> <b>$routeonaveragefeedback</b></b></td><td>$gymrouteonaveragefeedback </td></tr>\n";
	print "<tr><td>Hard:</td><td> <b>$routehardaveragefeedback</b></b></td><td>$gymroutehardaveragefeedback</td></tr>\n";
	print "<tr><td>Total:</td><td> <b>$routetotalaveragefeedback</b></b></td><td>$gymroutetotalaveragefeedback</td></tr>\n";

	print "</table>";

	print "<br><br>";

	## PRINT BOULDERS

	#### Print Boulder Feedback Averaged by Grade Graph
	$title = "Boulder%20Feedback%20Average%20by%20Grade";
	$amount = "Score";
	$legend1 = "$setter";
	$legend2 = "Gym%20Average";
	$legend3 = "";
	$legend4 = "";
	$maxvalue = "6";
	$ticks = "40";
	$type = "boulderaveragebygrade";
	$columncounter = "1";

	foreach (@bouldergradeindex) {
		++$columncounter;
		++$columncounter;
	}

	print "<table border=\"1\" style=\"width:1100px\">";
	print "<tr><td colspan=5><b>Boulders Set:</b></td><td rowspan=\"$columncounter\" align=center><img src=grapher.cgi?title=$title&amount=$amount&monthstart=$monthstart&duration=$duration&legend1=$legend1&legend2=$legend2&legend3=$legend3&legend4=$legend4&maxvalue=$maxvalue&ticks=$ticks&type=$type&setterid=$setterid&reviewdate=$reviewdate>";

	#### Print Number of Boulders Set By Grade Graph
	$title = "Number%20of%20Boulders%20Set%20by%20Grade";
	$amount = "Quantity";
	$legend1 = "Boulders%20Set";
	$legend2 = "";
	$legend3 = "";
	$legend4 = "";
	$maxvalue = "30";
	$ticks = "60";
	$type = "bouldernumberset";

	print "<br><img src=grapher.cgi?title=$title&amount=$amount&monthstart=$monthstart&duration=$duration&legend1=$legend1&legend2=$legend2&legend3=$legend3&legend4=$legend4&maxvalue=$maxvalue&ticks=$ticks&type=$type&setterid=$setterid&reviewdate=$reviewdate><br>";

	print "<hr><br><b>Comments:</b><br>";

	foreach (@bouldercomments) {
		if ($_) {
			print "$_<br>";
		}
	}

	print "</tr></td>";

	foreach (@bouldergradeindex) {
		### Get Percentage set
		if ($bouldernumberset[$boulderprintcounter]) {
			$percentset = $bouldernumberset[$boulderprintcounter] / $bouldertotalnumberset[$boulderprintcounter];
			$percentset = sprintf '%.0f', 100 * $percentset;
		}
		else {
			$percentset = "0";
		}

		print "<tr>
				<th rowspan=\"2\"><b>$_:</b></th>
				<th colspan=\"3\"> $bouldernumberset[$boulderprintcounter] / $bouldertotalnumberset[$boulderprintcounter] ($percentset%)</th>
			</tr>";

		print "<tr>
				<td colspan=\"2\" align=\"center\"><b>S:</b> $settertotals[$boulderprintcounter] </td>
				<td colspan=\"2\" align=\"center\"><b>GA:</b> $gymtotals[$boulderprintcounter] </td>
			</tr>";
		++$boulderprintcounter;
	}

	print "</table>";


	### PRINT ROUTES

	#### Print Route Feedback Averaged by Grade Graph
	$title = "Route%20Feedback%20Average%20by%20Grade";
	$amount = "Score";
	$legend1 = "$setter";
	$legend2 = "Gym%20Average";
	$legend3 = "";
	$legend4 = "";
	$maxvalue = "6";
	$ticks = "40";
	$type = "routeaveragebygrade";
	$columncounter = "1";

	foreach (@routegradeindex) {
		++$columncounter;
		++$columncounter;
	}

	print "<br><br><table border=\"1\" style=\"width:1100px\">";
	print "<tr><td colspan=5><b>Routes Set:</b></td><td rowspan=\"$columncounter\" align=center><img src=grapher.cgi?title=$title&amount=$amount&monthstart=$monthstart&duration=$duration&legend1=$legend1&legend2=$legend2&legend3=$legend3&legend4=$legend4&maxvalue=$maxvalue&ticks=$ticks&type=$type&setterid=$setterid&reviewdate=$reviewdate>";

	#### Print Number of Routes Set By Grade Graph
	$title = "Number%20of%20Routes%20Set%20by%20Grade";
	$amount = "Quantity";
	$legend1 = "Routes%20Set";
	$legend2 = "";
	$legend3 = "";
	$legend4 = "";
	$maxvalue = "20";
	$ticks = "40";
	$type = "routenumberset";

	print "<br><img src=grapher.cgi?title=$title&amount=$amount&monthstart=$monthstart&duration=$duration&legend1=$legend1&legend2=$legend2&legend3=$legend3&legend4=$legend4&maxvalue=$maxvalue&ticks=$ticks&type=$type&setterid=$setterid&reviewdate=$reviewdate><br>";
	print "<hr><br><b>Comments:</b><br>";

	foreach (@routecomments) {
		if ($_) {
			print "$_<br>";
		}
	}

	print "</tr></td>";

	foreach (@routegradeindex) {
		### Get Percentage set
		if ($routenumberset[$routeprintcounter]) {
			$percentset = $routenumberset[$routeprintcounter] / $routetotalnumberset[$routeprintcounter];
			$percentset = sprintf '%.0f', 100 * $percentset;
		}
		else {
			$percentset = "0";
		}
		print "<tr>
				<th rowspan=\"2\"><b>$_:</b></th>
				<th colspan=\"3\"> $routenumberset[$routeprintcounter] / $routetotalnumberset[$routeprintcounter] ($percentset%) </th>
			</tr>";
		print "<tr>
				<td colspan=\"2\" align=\"center\"><b>S:</b> $routesettertotals[$routeprintcounter]  </td>
				<td colspan=\"2\" align=\"center\"><b>GA:</b> $routegymtotals[$routeprintcounter] </td>
			</tr>";
		++$routeprintcounter;
	}

	print "</table>";

}


############# Run View Database if Selected ################

elsif ($action eq "team") {

	### Start Form for Reporting Feedback.
	print "Print Team Report<br>";
	print "<form action=\"rfas.cgi\" name=\"PrintTeamReportForm\" method=\"GET\">\n";

	### Date Boxes
	print '<br><br>Review Date: <input type="text" name=reviewdate id="datepicker" autocomplete="off"/><br><br>';

	### Print Available Date Range
	$sql = "SELECT Date FROM `Feedback_Data` ORDER BY Date DESC LIMIT 1;";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";
	$newest_date = $sth->fetchrow_array;

	$sql = "SELECT Date FROM `Feedback_Data` ORDER BY Date ASC LIMIT 1;";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";
	$oldest_date = $sth->fetchrow_array;

	print "Data available from <b>$oldest_date</b> to <b>$newest_date</b>.<br><br>";

	### Print 6 months or year
	print "Length of Review:<br>";
	print '<input type="radio" name="duration" value="sixmonths"> 6 Months<br>';
	print '<input type="radio" name="duration" value="oneyear"> 1 Year<br>';

	###Make submit/reset buttons and finish form
	print "<br><br><br>";
	print submit ('action', 'TeamReport');
	print reset;
	print "</form>";

}

elsif ($action eq "TeamReport") {

	$setter = $q->param('setter');
	$reviewdate = $q->param('reviewdate');
	$duration = $q->param('duration');
	@softquality = ("Soft1.Quality", "Soft2.Quality", "Soft3.Quality", "Soft4.Quality", "Soft5.Quality", "Soft6.Quality", "Soft7.Quality", "Soft8.Quality");
	@onquality = ("On1.Quality", "On2.Quality", "On3.Quality", "On4.Quality", "On5.Quality", "On6.Quality", "On7.Quality", "On8.Quality");
	@hardquality = ("Hard1.Quality", "Hard2.Quality", "Hard3.Quality", "Hard4.Quality", "Hard5.Quality", "Hard6.Quality", "Hard7.Quality", "Hard8.Quality");

	if ($duration eq "sixmonths") {
		($month, $day, $year) = split '/', $reviewdate;
		$sixmonthsdate = DateTime->new( year => $year, month => $month, day => $day );
		$sixmonthsdate->subtract( months => 6 );
		($year, $month, $day) = split (m[-], $sixmonthsdate);
		$day = substr $day, 0, 2;
		$sixmonthsdate = "$month/$day/$year";
	}

	elsif ($duration eq "oneyear") {
		($month, $day, $year) = split '/', $reviewdate;
		$yeardate = DateTime->new( year => $year, month => $month, day => $day );
		$yeardate->subtract( months => 12 );
		($year, $month, $day) = split (m[-], $yeardate);
		$day = substr $day, 0, 2;
		$sixmonthsdate = "$month/$day/$year";
	}

	else {
		die "You must select a length of time."
	}

	### Start Page
	print "Between <b>$sixmonthsdate - $reviewdate</b>:<br><br>\n";

	### Reformat Dates
	($month, $day, $year) = split(m[/], $sixmonthsdate);
	$sixmonthsdate = "$year-$month-$day";
	($month, $day, $year) = split(m[/], $reviewdate);
	$reviewdate = "$year-$month-$day";

	## Soft Boulders
	$softfeedbackcounter = "0";
	foreach (@softquality) {
		## Query For Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'B\' AND `Date` BETWEEN \"$sixmonthsdate\" AND  \"$reviewdate\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		@counter = ();
		while (@row = $sth->fetchrow_array) {
			push (@counter, @row);
		}

		foreach (@counter) {
			if ($_ ne "") {
				++$softfeedbackcounter;
				++$boulderfeedbacktotalcounter;
			}
		}
	}

	## On Boulders
	$onfeedbackcounter = "0";
	foreach (@onquality) {
		## Query For Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'B\' AND `Date` BETWEEN \"$sixmonthsdate\" AND  \"$reviewdate\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		while (@row = $sth->fetchrow_array) {
			push (@counter, @row);
		}

		foreach (@counter) {
			if ($_ ne "") {
				++$onfeedbackcounter;
				++$boulderfeedbacktotalcounter;
			}
		}
	}

	## Hard Boulders
	$hardfeedbackcounter = "0";
	foreach (@hardquality) {
		## Query For Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'B\' AND `Date` BETWEEN \"$sixmonthsdate\" AND  \"$reviewdate\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		@counter = ();
		while (@row = $sth->fetchrow_array) {
			push (@counter, @row);
		}

		foreach (@counter) {
			if ($_ ne "") {
				++$hardfeedbackcounter;
				++$boulderfeedbacktotalcounter;
			}
		}
	}

	$softboulder = $softfeedbackcounter / $boulderfeedbacktotalcounter;
	$softboulder = substr $softboulder, 2, 2;

	$onboulder = $onfeedbackcounter / $boulderfeedbacktotalcounter;
	$onboulder = substr $onboulder, 2, 2;

	$hardboulder = $hardfeedbackcounter / $boulderfeedbacktotalcounter;
	$hardboulder = substr $hardboulder, 2, 2;

	## Soft Routes
	$softfeedbackcounter = "0";
	foreach (@softquality) {
		## Query For Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'R\' AND `Date` BETWEEN \"$sixmonthsdate\" AND  \"$reviewdate\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		@counter = ();
		while (@row = $sth->fetchrow_array) {
			push (@counter, @row);
		}

		foreach (@counter) {
			if ($_ ne "") {
				++$softfeedbackcounter;
				++$routefeedbacktotalcounter;
			}
		}
	}

	## On Routes
	$onfeedbackcounter = "0";
	foreach (@onquality) {
		## Query For Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'R\' AND `Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		while (@row = $sth->fetchrow_array) {
			push (@counter, @row);
		}

		foreach (@counter) {
			if ($_ ne "") {
				++$onfeedbackcounter;
				++$routefeedbacktotalcounter;
			}
		}
	}

	## Hard Route
	$hardfeedbackcounter = "0";
	foreach (@hardquality) {
		## SQL Query For Feedback
		$sql = "SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'R\' AND`Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\"";
		$sth = $dbh->prepare($sql);
		$sth->execute
		or die "SQL Error: $DBI::errstr\n";

		@counter = ();
		while (@row = $sth->fetchrow_array) {
			push (@counter, @row);
		}

		foreach (@counter) {
			if ($_ ne "") {
				++$hardfeedbackcounter;
				++$routefeedbacktotalcounter;
			}
		}
	}


	$softroute = $softfeedbackcounter / $routefeedbacktotalcounter;
	$softroute = substr $softroute, 2, 2;

	$onroute = $onfeedbackcounter / $routefeedbacktotalcounter;
	$onroute = substr $onroute, 2, 2;

	$hardroute = $hardfeedbackcounter / $routefeedbacktotalcounter;
	$hardroute = substr $hardroute, 2, 2;


	#### ORIGINAL GRADE FUNCTIONS

	$uproutes = "0";
	$downroutes = "0";
	$upboulder = "0";
	$downboulder = "0";

	###Routes that got upgraded
	$sql = "SELECT `OriginalGrade` FROM `Feedback_Data` WHERE `Type` = \'R\' AND `OriginalGrade` < `Grade` AND `Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\"";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";

	while (@row = $sth->fetchrow_array) {
		if (@row[0] != "") {
			++$uproutes;
		}
	}

	###Routes that got downgraded
	$sql = "SELECT `OriginalGrade` FROM `Feedback_Data` WHERE `Type` = \'R\' AND `OriginalGrade` > `Grade` AND `Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\"";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";

	while (@row = $sth->fetchrow_array) {
		if (@row[0] != "") {
			++$downroutes;
		}
	}

	###Boulder that got upgraded
	$sql = "SELECT `OriginalGrade` FROM `Feedback_Data` WHERE `Type` = \'B\' AND `OriginalGrade` < `Grade` AND `Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\"";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";

	while (@row = $sth->fetchrow_array) {
		if (@row[0] != "") {
			++$upboulder;
		}
	}

	###Boulder that got downgraded
	$sql = "SELECT `OriginalGrade` FROM `Feedback_Data` WHERE `Type` = \'B\' AND `OriginalGrade` > `Grade` AND `Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\"";
	$sth = $dbh->prepare($sql);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";

	while (@row = $sth->fetchrow_array) {
		if (@row[0] != "") {
			++$downboulder;
		}
	}

	#### DATE FUNCTIONS
	$date = DateTime->today;
	##Set Date 6 months before now
	($year, $month, $day) = split '-', $date;
	($day, $scrap) = split 'T', $day;
	$currentdate = "$month/$day/$year";
	$pastdate = DateTime->new( year => $year, month => $month, day => $day );
	$pastdate->subtract( months => 6 );
	($year, $month, $day) = split (m[-], $pastdate);
	$day = substr $day, 0, 2;
	$sixmonthsdate = "$month/$day/$year";

	### PRINT FEEDBACK
	print "<b>$softboulder%</b> of boulder feedback was soft.<br>";
	print "<b>$onboulder%</b> of boulder feedback was on grade.<br>";
	print "<b>$hardboulder%</b> of boulder feedback was hard.<br><br>";

	print "<b>$softroute%</b> of route feedback was soft.<br>";
	print "<b>$onroute%</b> of route feedback was on grade.<br>";
	print "<b>$hardroute%</b> of route feedback was hard.<br><br>";

	print "<b>$upboulder</b> boulders were upgraded and <b>$downboulder</b>  were downgraded.<br>";
	print "<b>$uproutes</b> routes were upgraded and <b>$downroutes</b> were downgraded.<br>";

}

########## Print error if there is an unknown option ################

else {
	print "There was an error. Please retry your request."
}

### End HTML
print end_html;
