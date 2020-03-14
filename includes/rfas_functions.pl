### Define Subroutines
sub RunSQL {
	$sth = $dbh->prepare(@_);
	$sth->execute
	or die "SQL Error: $DBI::errstr\n";
}

sub PrintDateBox {
	print "<br><br>@_ Date: <input type='text' name=reviewdate id='datepicker' autocomplete='off'/><br><br>";
}

sub PrintFeedbackBoxes {
	$type = $_;
	print "$type: \n";
	foreach (1..8) {
		print "<input type='text' maxlength='3' size='2' name='$type$_'>";
	}
	print "<p>"
}

sub PrintSubmit {
	print "<br><br><br>";
	print submit ('action', "@_");
	print reset;
	print "</form>";
}

sub PrintSetterBox {
	print "<select name=\"$_\">\n
			<option value=\"Blank\"> </option>\n";
	RunSQL("SELECT `Name` FROM `Setter_Index`");
	while (@row = $sth->fetchrow_array) {
		foreach (@row) {
			$inactivesetter = m\#\;
			if (!$inactivesetter) {
				print "<option value=\"$_\">$_</option>\n";
			}
		}
	}
	print "</select>";
}

sub PrintDataAvailableBox {
    RunSQL("SELECT Date FROM `Feedback_Data` ORDER BY Date DESC LIMIT 1;");
    $newest_date = $sth->fetchrow_array;
    RunSQL("SELECT Date FROM `Feedback_Data` ORDER BY Date ASC LIMIT 1;");
    $oldest_date = $sth->fetchrow_array;
    print "Data available from <b>$oldest_date</b> to <b>$newest_date</b>.<br><br>";
}

sub PrintLengthOfReview {
    print "Length of Review:<br>";
    print '<input type="radio" name="duration" value="sixmonths"> 6 Months<br>';
    print '<input type="radio" name="duration" value="oneyear"> 1 Year<br>';
}

1;
