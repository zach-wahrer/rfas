#!/usr/bin/perl -w

# Routesetting Feedback Analysis Software v0.5
# Written by Zach Wahrer

### Load Modules ###
use CGI qw(:standard);
use DBI;
use Scalar::Util qw(looks_like_number);
use DateTime;

### Import subroutines ###
require '/usr/rfas/rfas_functions.pl';

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
$action = $q->param('action');

## Start HTML
print "Content-type:  text/html\n\n";
print "<head>\n";
print "<title>RFAS - V0.5</title>\n";
if (defined($action)) {
	PrintCalendarWidgit();
}
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
	print "Setter: \n";
	foreach ('setter1', 'setter2', 'setter3') {
		PrintSetterBox($_)
	}

	PrintDateBox();

	### Print Route Rating Boxes
	RunSQL("SELECT `Route Grade` FROM `Route_Grade_Index`");

	while (@row = $sth->fetchrow_array) {
		push (@routegrade, @row);
	}

	print "<br><br>Route Rating: \n";
	print "<select name=\"routegrade\">\n
			<option value=\"Blank\"> </option>\n";
	foreach (@routegrade) {
		print "<option value=\"$_\">$_</option>\n";
	}
	print "</select>";

	print "<p>Orignal Route Rating:\n";
	print "<select name=\"routeoriginalgrade\">\n
			<option value=\"Blank\"> </option>\n";
	foreach (@routegrade) {
		print "<option value=\"$_\">$_</option>\n";
	}
	print "</select>\n\n";

	###Print Boulder Rating Boxes
	RunSQL("SELECT `Boulder Grade` FROM `Boulder_Grade_Index`");

	while (@row = $sth->fetchrow_array) {
		push (@bouldergrade, @row);
	}

	print "<br><br><br>Boulder Rating: \n";
	print "<select name=\"bouldergrade\">\n
			<option value=\"Blank\"> </option>\n";
	foreach (@bouldergrade) {
		print "<option value=\"$_\">$_</option>\n";
	}
	print "</select>";

	print "<p>Orignal Boulder Rating:\n";
	print "<select name=\"boulderoriginalgrade\">\n
			<option value=\"Blank\"> </option>\n";
	foreach (@bouldergrade) {
		print "<option value=\"$_\">$_</option>\n";
	}
	print "</select>\n\n";

	###Feedback Matrix
	print "<br><br><br>Feedback:<p>\n";

	foreach('Soft', 'On', 'Hard') {
		PrintFeedbackBoxes($_);
	}

	foreach(1..8) {
		print "Comment $_: <input type='text' maxlength='100' size='50' name='Comment$_'><br>";
	}

	PrintSubmit('Submit');

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


	if ($setter1 eq "Blank") {
		die "You have to enter a First Setter!";
	}
	else {
		RunSQL("SELECT `ID` FROM `Setter_Index` WHERE `Name` = \"$setter1\"");
		$setter1 = $sth->fetchrow_array;

		if ($setter2 ne "Blank") {
			RunSQL("SELECT `ID` FROM `Setter_Index` WHERE `Name` = \"$setter2\"");
			$setter2 = $sth->fetchrow_array;
		}
		else {
			$setter2 = undef;
		}

		if ($setter3 ne "Blank") {
			RunSQL("SELECT `ID` FROM `Setter_Index` WHERE `Name` = \"$setter3\"");
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

	###### ERROR CHECKING ######
	if ($routegrade eq "Blank" and $routeoriginalgrade eq "Blank" and $bouldergrade eq "Blank" and $boulderoriginalgrade eq "Blank") {
		die "You have to enter a Grade!";
	}
	if ($routeoriginalgrade ne "Blank" and $routegrade eq "Blank") {
		die "You have to enter a Route Grade with an Original Grade!";
	}
	if ($boulderoriginalgrade ne "Blank" and $bouldergrade eq "Blank") {
		die "You have to enter a Bouldering Grade with an Original Grade!";
	}
	if ($bouldergrade ne "Blank" and $routegrade ne "Blank") {
		die "You cannot enter both Bouldering and Route grades at the same time.";
	}

	### Look up route grade ID and original grade if route is selected
	if ($routegrade ne "Blank") {
		RunSQL("SELECT `ID` FROM `Route_Grade_Index` WHERE `Route Grade` = \"$routegrade\"");
		$routegrade = $sth->fetchrow_array;
		$type = "R";
		$grade = $routegrade;
	}
	if ($routeoriginalgrade ne "Blank") {
		RunSQL("SELECT `ID` FROM `Route_Grade_Index` WHERE `Route Grade` = \"$routeoriginalgrade\"");
		$routeoriginalgrade = $sth->fetchrow_array;
		$originalgrade = $routeoriginalgrade;
	}

	### Look up boulder grade ID and original grade if boulder is selected
	if ($bouldergrade ne "Blank") {
		RunSQL("SELECT `ID` FROM `Boulder_Grade_Index` WHERE `Boulder Grade` = \"$bouldergrade\"");
		$bouldergrade = $sth->fetchrow_array;
		$type = "B";
		$grade = $bouldergrade;
	}
	if ($boulderoriginalgrade ne "Blank") {
		RunSQL("SELECT `ID` FROM `Boulder_Grade_Index` WHERE `Boulder Grade` = \"$boulderoriginalgrade\"");
		$boulderoriginalgrade = $sth->fetchrow_array;
		$originalgrade = $boulderoriginalgrade;
	}

	### Make sure Soft/On/Hard + Quality ratings aren't <5 or less than 0 or a non-number ###
	foreach ($Soft1, $Soft2, $Soft3, $Soft4, $Soft5, $Soft6, $Soft7, $Soft8,
					$On1, $On2, $On3, $On4, $On5, $On6, $On7, $On8,
					$Hard1, $Hard2, $Hard3, $Hard4, $Hard5, $Hard6, $Hard7, $Hard8) {
		if ($_ ne "x" and $_ ne "" and ! looks_like_number $_) {
			die "You entered an improperly formatted feedback score.";
		}
		elsif ($_ > "5" or $_ < "0") {
			die "You cannot enter a feedback score higher than 5 or less than 0."
		}
	}

	### Put Data Into Database ###
	RunSQL("INSERT INTO `route_feedback`.`Feedback_Data` (`Index`, `Name1`, `Name2`, `Name3`, `Type`, `Grade`, `OriginalGrade`, `Date`, `Soft1.Quality`, `Soft2.Quality`, `Soft3.Quality`, `Soft4.Quality`, `Soft5.Quality`, `Soft6.Quality`, `Soft7.Quality`, `Soft8.Quality`, `On1.Quality`, `On2.Quality`, `On3.Quality`, `On4.Quality`, `On5.Quality`, `On6.Quality`, `On7.Quality`, `On8.Quality`, `Hard1.Quality`, `Hard2.Quality`, `Hard3.Quality`, `Hard4.Quality`, `Hard5.Quality`, `Hard6.Quality`, `Hard7.Quality`, `Hard8.Quality`, `Comment1`, `Comment2`, `Comment3`, `Comment4`, `Comment5`, `Comment6`, `Comment7`, `Comment8`)
		VALUES (NULL, '$setter1', '$setter2', '$setter3', '$type', '$grade', '$originalgrade', '$date', '$Soft1', '$Soft2', '$Soft3', '$Soft4', '$Soft5', '$Soft6', '$Soft7', '$Soft8', '$On1', '$On2', '$On3', '$On4', '$On5', '$On6', '$On7', '$On8', '$Hard1', '$Hard2', '$Hard3', '$Hard4', '$Hard5', '$Hard6', '$Hard7', '$Hard8', '$Comment1', '$Comment2', '$Comment3', '$Comment4', '$Comment5', '$Comment6', '$Comment7', '$Comment8');");

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

	print "Setter: \n";
	PrintSetterBox('setter');

	PrintDateBox('Review');

	PrintDataAvailableBox();

	PrintLengthOfReview();

	PrintSubmit('Report');

}


### Print Feedback Report if Setter is Selected
elsif ($action eq "Report") {

	### Get/Set Variables
	$setter = $q->param('setter');
	$reviewdate = $q->param('reviewdate');
	$duration = $q->param('duration');

	@softquality = ("Soft1.Quality", "Soft2.Quality", "Soft3.Quality", "Soft4.Quality",
			"Soft5.Quality", "Soft6.Quality", "Soft7.Quality", "Soft8.Quality");

	@onquality = ("On1.Quality", "On2.Quality", "On3.Quality", "On4.Quality",
				"On5.Quality", "On6.Quality", "On7.Quality", "On8.Quality");

	@hardquality = ("Hard1.Quality", "Hard2.Quality", "Hard3.Quality", "Hard4.Quality",
			"Hard5.Quality", "Hard6.Quality", "Hard7.Quality", "Hard8.Quality");

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
	RunSQL("SELECT `ID` FROM `Setter_Index` WHERE `Name` = \"$setter\";");
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

	foreach (@softquality) {
		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\");");
		@softqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@softqualityratings, @row);
		}
		push (@softratings, @softqualityratings);

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\';");
		@gymsoftqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymsoftqualityratings, @row);
		}
		push (@gymsoftratings, @gymsoftqualityratings);
	}

	$softaverage = FeedbackAverage(@softratings);
	push (@totalaverage, @softratings);

	$gymsoftaverage = FeedbackAverage(@gymsoftratings);
	push (@gymtotalaverage, @gymsoftratings);


	foreach (@onquality) {
		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\");");
		@onqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@onqualityratings, @row);
		}
		push (@onratings, @onqualityratings);

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\';");
		@gymonqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymonqualityratings, @row);
		}
		push (@gymonratings, @gymonqualityratings);
	}

	$onaverage = FeedbackAverage(@onratings);
	push (@totalaverage, @onratings);

	$gymonaverage = FeedbackAverage(@gymonratings);
	push (@gymtotalaverage, @gymonratings);


	foreach (@hardquality) {
		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\");");
		@hardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@hardqualityratings, @row);
		}
			push (@hardratings, @hardqualityratings);

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\'");
		@gymhardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymhardqualityratings, @row);
		}
		push (@gymhardratings, @gymhardqualityratings);
	}

	$hardaverage = FeedbackAverage(@hardratings);
	push (@totalaverage, @hardratings);

	$gymhardaverage = FeedbackAverage(@gymhardratings);
	push (@gymtotalaverage, @gymhardratings);

	$totalaverage = FeedbackAverage(@totalaverage);
	$gymtotalaverage = FeedbackAverage(@gymtotalaverage);

	$softaveragefeedback = sprintf "%.2f", $softaverage;
	$onaveragefeedback = sprintf "%.2f", $onaverage;
	$hardaveragefeedback = sprintf "%.2f", $hardaverage;
	$totalaveragefeedback = sprintf "%.2f", $totalaverage;
	$gymsoftaveragefeedback = sprintf "%.2f", $gymsoftaverage;
	$gymonaveragefeedback = sprintf "%.2f", $gymonaverage;
	$gymhardaveragefeedback = sprintf "%.2f", $gymhardaverage;
	$gymtotalaveragefeedback = sprintf "%.2f", $gymtotalaverage;


	################ BOULDER AVERAGES ################

	foreach (@softquality) {
		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"B\")");
		@bouldersoftqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@bouldersoftqualityratings, @row);
		}
		push (@bouldersoftratings, @bouldersoftqualityratings);

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"B\")");
		@gymbouldersoftqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymbouldersoftqualityratings, @row);
		}
		push (@gymbouldersoftratings, @gymbouldersoftqualityratings);
	}

	$bouldersoftaverage = FeedbackAverage(@bouldersoftratings);
	push (@bouldertotalaverage, @bouldersoftratings);

	$gymbouldersoftaverage = FeedbackAverage(@gymbouldersoftratings);
	push (@gymbouldertotalaverage, @gymbouldersoftratings);


	foreach (@onquality) {
		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"B\")");
		@boulderonqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@boulderonqualityratings, @row);
		}
		push (@boulderonratings, @boulderonqualityratings);

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"B\")");
		@gymboulderonqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymboulderonqualityratings, @row);
		}
		push (@gymboulderonratings, @gymboulderonqualityratings);
	}

	$boulderonaverage = FeedbackAverage(@boulderonratings);
	push (@bouldertotalaverage, @boulderonratings);

	$gymboulderonaverage = FeedbackAverage(@gymboulderonratings);
	push (@gymbouldertotalaverage, @gymboulderonratings);


	foreach (@hardquality) {
		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"B\")");
		@boulderhardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@boulderhardqualityratings, @row);
		}
			push (@boulderhardratings, @boulderhardqualityratings);

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"B\")");
		@gymboulderhardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymboulderhardqualityratings, @row);
		}
		push (@gymboulderhardratings, @gymboulderhardqualityratings);
	}

	$boulderhardaverage = FeedbackAverage(@boulderhardratings);
	push (@bouldertotalaverage, @boulderhardratings);

	$gymboulderhardaverage = FeedbackAverage(@gymboulderhardratings);
	push (@gymbouldertotalaverage, @gymboulderhardratings);

	$bouldertotalaverage = FeedbackAverage(@bouldertotalaverage);
	$gymbouldertotalaverage = FeedbackAverage(@gymbouldertotalaverage);

	$bouldersoftaveragefeedback = sprintf "%.2f", $bouldersoftaverage;
	$boulderonaveragefeedback = sprintf "%.2f", $boulderonaverage;
	$boulderhardaveragefeedback = sprintf "%.2f", $boulderhardaverage;
	$bouldertotalaveragefeedback = sprintf "%.2f", $bouldertotalaverage;
	$gymbouldersoftaveragefeedback = sprintf "%.2f", $gymbouldersoftaverage;
	$gymboulderonaveragefeedback = sprintf "%.2f", $gymboulderonaverage;
	$gymboulderhardaveragefeedback = sprintf "%.2f", $gymboulderhardaverage;
	$gymbouldertotalaveragefeedback = sprintf "%.2f", $gymbouldertotalaverage;


	################## ROUTE AVERAGES ###############

	foreach (@softquality) {
		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"R\")");
		@routesoftqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@routesoftqualityratings, @row);
		}
		push (@routesoftratings, @routesoftqualityratings);

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"R\")");
		@gymroutesoftqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymroutesoftqualityratings, @row);
		}
		push (@gymroutesoftratings, @gymroutesoftqualityratings);
	}

	$routesoftaverage = FeedbackAverage(@routesoftratings);
	push (@routetotalaverage, @routesoftratings);

	$gymroutesoftaverage = FeedbackAverage(@gymroutesoftratings);
	push (@gymroutetotalaverage, @gymroutesoftratings);


	foreach (@onquality) {
		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"R\");");
		@routeonqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@routeonqualityratings, @row);
		}
		push (@routeonratings, @routeonqualityratings);

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"R\");");
		@gymrouteonqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymrouteonqualityratings, @row);
		}
		push (@gymrouteonratings, @gymrouteonqualityratings);
	}

	$routeonaverage = FeedbackAverage(@routeonratings);
	push (@routetotalaverage, @routeonratings);

	$gymrouteonaverage = FeedbackAverage(@gymrouteonratings);
	push (@gymroutetotalaverage, @gymrouteonratings);


	foreach (@hardquality) {
		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"R\");");
		@routehardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@routehardqualityratings, @row);
		}
		push (@routehardratings, @routehardqualityratings);

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"R\");");
		@gymroutehardqualityratings = ();
		while (@row = $sth->fetchrow_array) {
			push (@gymroutehardqualityratings, @row);
		}
		push (@gymroutehardratings, @gymroutehardqualityratings);
	}

	$routehardaverage = FeedbackAverage(@routehardratings);
	push (@routetotalaverage, @routehardratings);

	$gymroutehardaverage = FeedbackAverage(@gymroutehardratings);
	push (@gymroutetotalaverage, @gymroutehardratings);

	$routetotalaverage = FeedbackAverage(@routetotalaverage);
	$gymroutetotalaverage = FeedbackAverage(@gymroutetotalaverage);

	$routesoftaveragefeedback = sprintf "%.2f", $routesoftaverage;
	$routeonaveragefeedback = sprintf "%.2f", $routeonaverage;
	$routehardaveragefeedback = sprintf "%.2f", $routehardaverage;
	$routetotalaveragefeedback = sprintf "%.2f", $routetotalaverage;
	$gymroutesoftaveragefeedback = sprintf "%.2f", $gymroutesoftaverage;
	$gymrouteonaveragefeedback = sprintf "%.2f", $gymrouteonaverage;
	$gymroutehardaveragefeedback = sprintf "%.2f", $gymroutehardaverage;
	$gymroutetotalaveragefeedback = sprintf "%.2f", $gymroutetotalaverage;


	########## BOULDER % OF GRADE SET W/ FEEDBACK ###########

	@feedbackquality = (@softquality,@onquality,@hardquality);

	RunSQL("SELECT  `ID` FROM  `Boulder_Grade_Index`;");
	while (@row = $sth->fetchrow_array) {
		push (@boulderindexgrades, @row);
	}

	foreach (@boulderindexgrades) {

		### For Number Set Per Grade ###
		RunSQL("SELECT `Index` FROM `Feedback_Data` WHERE `Grade` = \"$_\" AND`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"B\");");
		$bouldernumberset = "0";
		while (@row = $sth->fetchrow_array) {
			++$bouldernumberset;
		}
		push (@bouldernumberset, $bouldernumberset);

		### For Total Set Per Grade ###
		RunSQL("SELECT `Index` FROM `Feedback_Data` WHERE `Grade` = \"$_\" AND`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"B\");");
		$bouldertotalnumberset = "0";
		while (@row = $sth->fetchrow_array) {
			++$bouldertotalnumberset;
		}
		push (@bouldertotalnumberset, $bouldertotalnumberset);

		### Make Grade Array ###
		RunSQL("SELECT `Boulder Grade` FROM `Boulder_Grade_Index` WHERE `ID` = \"$_\";");
		while (@row = $sth->fetchrow_array) {
			push (@bouldergradeindex, @row);
		}

		### Get Feedback For Setter ###
		$grade = $_;
		@boulderfeedbackgrade = ();
		foreach (@feedbackquality) {
			RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Grade` = \"$grade\" AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"B\");");
			while (@row = $sth->fetchrow_array) {
				push (@boulderfeedbackgrade, @row);
			}
		}

		$setterfeedbacktotal = "0";
		$settertotalcounter = "0";
		$settertotalaverage = "0";

		### Average Setter Feedback
		$settertotalaverage = FeedbackAverage(@boulderfeedbackgrade);
		$settertotalaverage = sprintf "%.2f", $settertotalaverage;
		push (@settertotals, $settertotalaverage);

		### Get GYM Feedback Average ###
		$grade = $_;
		@boulderfeedbackgrade = ();
		foreach (@feedbackquality) {
			RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Grade` = \"$grade\" AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Type` = \"B\");");
			while (@row = $sth->fetchrow_array) {
				push (@boulderfeedbackgrade, @row);
			}

		}

		$gymtotalaverage = "0";
		$gymtotalaverage = FeedbackAverage(@boulderfeedbackgrade);
		$gymtotalaverage = sprintf "%.2f", $gymtotalaverage;
		push (@gymtotals, $gymtotalaverage);

	}

	########## ROUTE % OF GRADE SET W/ FEEDBACK ###########

	RunSQL("SELECT  `ID` FROM  `Route_Grade_Index`;");
	while (@row = $sth->fetchrow_array) {
		push (@routeindexgrades, @row);
	}

	foreach (@routeindexgrades) {
		### For Number Set Per Grade ###
		RunSQL("SELECT `Index` FROM `Feedback_Data` WHERE `Grade` = \"$_\" AND`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"R\");");
		$routenumberset = "0";
		while (@row = $sth->fetchrow_array) {
			++$routenumberset;
		}
		push (@routenumberset, $routenumberset);

		### For Total Set Per Grade ###
		RunSQL("SELECT `Index` FROM `Feedback_Data` WHERE `Grade` = \"$_\" AND`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\' AND (`Type` = \"R\");");
		$routetotalnumberset = "0";
		while (@row = $sth->fetchrow_array) {
			++$routetotalnumberset;
		}
		push (@routetotalnumberset, $routetotalnumberset);

		### Make Grade Array ###
		RunSQL("SELECT `Route Grade` FROM `Route_Grade_Index` WHERE `ID` = \"$_\";");
		while (@row = $sth->fetchrow_array) {
			push (@routegradeindex, @row);
		}

		### Get Feedback For Setter ###
		$grade = $_;
		@routefeedbackgrade = ();
		foreach (@feedbackquality) {
			RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Grade` = \"$grade\" AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Type` = \"R\");");
			while (@row = $sth->fetchrow_array) {
				push (@routefeedbackgrade, @row);
			}
		}

		$settertotalaverage = "0";
		$settertotalaverage = FeedbackAverage(@routefeedbackgrade);
		$settertotalaverage = sprintf "%.2f", $settertotalaverage;
		push (@routesettertotals, $settertotalaverage);


		### Get GYM Feedback Average ###
		$grade = $_;
		@routefeedbackgrade = ();
		foreach (@feedbackquality) {
			RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Grade` = \"$grade\" AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Type` = \"R\");");
			while (@row = $sth->fetchrow_array) {
				push (@routefeedbackgrade, @row);
			}
		}

		$gymtotalaverage = "0";
		$gymtotalaverage = FeedbackAverage(@routefeedbackgrade);
		$gymtotalaverage = sprintf "%.2f", $gymtotalaverage;
		push (@routegymtotals, $gymtotalaverage);
	}


	########## GET COMMENTS #############

	$comments = "`Comment1`, `Comment2`, `Comment3`, `Comment4`, `Comment5`, `Comment6`, `Comment7`, `Comment8`";

	## BOULDERS

	RunSQL("SELECT $comments FROM `Feedback_Data` WHERE (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Type` = \"B\");");
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

	RunSQL("SELECT $comments FROM `Feedback_Data` WHERE (`Name1` = \"$setterid\" or `Name2` = \"$setterid\" or `Name3` = \"$setterid\") AND (`Date` BETWEEN  \'$sixmonthsdate\' AND  \'$reviewdate\') AND (`Type` = \"R\");");
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

	PrintDateBox('Review');

	PrintDataAvailableBox();

	PrintLengthOfReview();

	PrintSubmit('TeamReport');

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

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'B\' AND `Date` BETWEEN \"$sixmonthsdate\" AND  \"$reviewdate\";");
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

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'B\' AND `Date` BETWEEN \"$sixmonthsdate\" AND  \"$reviewdate\";");
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
		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'B\' AND `Date` BETWEEN \"$sixmonthsdate\" AND  \"$reviewdate\";");

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

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'R\' AND `Date` BETWEEN \"$sixmonthsdate\" AND  \"$reviewdate\";");
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

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'R\' AND `Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\";");
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

		RunSQL("SELECT `$_` FROM `Feedback_Data` WHERE `Type` = \'R\' AND`Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\";");
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
	RunSQL("SELECT `OriginalGrade` FROM `Feedback_Data` WHERE `Type` = \'R\' AND `OriginalGrade` < `Grade` AND `Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\";");
	while (@row = $sth->fetchrow_array) {
		if ($row[0] != "") {
			++$uproutes;
		}
	}

	###Routes that got downgraded
	RunSQL("SELECT `OriginalGrade` FROM `Feedback_Data` WHERE `Type` = \'R\' AND `OriginalGrade` > `Grade` AND `Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\";");
	while (@row = $sth->fetchrow_array) {
		if ($row[0] != "") {
			++$downroutes;
		}
	}

	###Boulder that got upgraded
	RunSQL("SELECT `OriginalGrade` FROM `Feedback_Data` WHERE `Type` = \'B\' AND `OriginalGrade` < `Grade` AND `Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\";");
	while (@row = $sth->fetchrow_array) {
		if ($row[0] != "") {
			++$upboulder;
		}
	}

	###Boulder that got downgraded
	RunSQL("SELECT `OriginalGrade` FROM `Feedback_Data` WHERE `Type` = \'B\' AND `OriginalGrade` > `Grade` AND `Date` BETWEEN  \"$sixmonthsdate\" AND  \"$reviewdate\";");
	while (@row = $sth->fetchrow_array) {
		if ($SSrow[0] != "") {
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
