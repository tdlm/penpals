#!/usr/bin/perl

$request_method = $ENV{'REQUEST_METHOD'};
$support="support\@nemisys\.com";

if ($request_method eq "GET") {
  $query_string = $ENV{'QUERY_STRING'};  
} else {
 read (STDIN, $query_string, $ENV{'CONTENT_LENGTH'});
}

@pairs=split(/&/, $query_string);
foreach $key_value (@pairs) {
  ($key, $value)=split(/=/, $key_value);
  $value=~tr/+/ /;
  $value=~s/%([\dA-Fa-f][\dA-Fa-f])/pack ("C", hex ($1))/eg;
  if (defined($FORM_DATA{$key})) {
    $FORM_DATA{$key}=join("\0", $FORM_DATA{$key}, $value);
   } else {
    $FORM_DATA{$key}=$value;
  }
}

open (PENPALS, "<penpals.dat") || die "Can't open file $!";
flock (PENPALS, 2);
@contents=<PENPALS>;
flock (PENPALS, 8);
close (PENPALS);


print "Content-type: text/html\n\n";

print <<EndOfHTML;
<html>
<head>
<title>Pen Pal Users</title>
</head>
<body bgcolor="#000000" text="#FFFFFF" link="#FFFFFF" vlink="#FFFFFF" alink="#FFFFFF" background="../bg2.gif">
<table border="0" cellspacing="0" bgcolor="#000000" cellpadding="10" width="50%" align="center">
  <tr>
    <td valign="top" colspan="2" height="20%" align="center"><p align="center">&nbsp;<br>
    <img src="../ntop.gif" alt="ntop.gif (7794 bytes)" width="525" height="175"><br>
    </p>
    <p align="center"><font face="arial" size="2">[ <a
    href="http://www.nemisys.com/services.html">Services</a> | <a
    href="http://www.nemisys.com/hosted.htm">Hosted Pages</a> | <a
    href="http://www.nemisys.com/cgi-bin/list.cgi?view=all">PenPal Section</a> | <a
    href="mailto:$support">Support</a> ]</font></td>
  </tr>
  <tr>
    <td width="30%" valign="top" height="80%"><table border="0" bgcolor="#333660"
    cellpadding="4" cellspacing="0" width="80%">
      <tr>
        <td nowrap><p align="left"><font face="arial" size="2"><strong>Site Links
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </strong></font></td>
      </tr>
      <tr>
        <td bgcolor="#404040" nowrap><font face="arial" size="2"><br>
        <a href="http://www.nemisys.com/services.html">Services</a></font><p><a
        href="http://www.nemisys.com/hosted.htm"><font face="arial" size="2">Hosted Pages</font></a></p>
        <p><a href="http://www.nemisys.com/cgi-bin/list.cgi?view=all"><font face="arial" size="2">PenPal
        Section</font></a></p>
        <p><font face="arial" size="2"><a href="mailto:$support">Support</a><br>
        <br>
        <a href="/cgi-bin/whois.pl">Whois lookup</a><br>
        <br>
        <a href="/cgi-bin/search.pl">Site Search</a><br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </font></td>
      </tr>
      <tr>
        <td bgcolor="#000000" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </td>
      </tr>
      <tr>
        <td bgcolor="#333660" nowrap><font face="arial" size="2"><strong>Outside Links</strong></font></td>
      </tr>
    </table>
    <p align="center"><img
    src="http://216.89.176.57/cgi-bin/Count.cgi?df=my.dat&amp;dd=HHHH&amp;ft=0" width="108"
    height="22" align="left"> </td>
    <td valign="top" height="80%" width="90%"><a name="news"></a><table border="0"
    bgcolor="#333660" cellspacing="0" width="80%">
      <tr>
        <td nowrap height="17"><font face="arial" size="2"><strong>nemesis internet systems: </strong><small>penpal section</small></font></td>
      </tr>
      <tr>
        <td bgcolor="#000000">
EndOfHTML

$count=0;

foreach $line (@contents) {
  ($ID, $name, $age, $sex, $location, $url, $email, $address, $prefer,
   $pref_sex, $interests, $comments)=split(/:;,.:/, $line);


if (($FORM_DATA{view} eq "all") or (($FORM_DATA{view} eq "female") and
 ($sex eq "Female")) or (($FORM_DATA{view} eq "male") and ($sex eq "Male")))
{

$temp_contents[$count]=("$ID :: $name :: $age :: $sex :: $location :: $pref_sex :: $prefer");
$count++;

}
}

# Bubble Sort @temp_contents by age.

$total=@temp_contents;

for ($i=0; $i<=$total; $i++) {
  for ($j=1; $j<=$total; $j++) {
    next if ($i==$j);
    ($ID, $name, $age, $sex, $location, $pref_sex, $prefer)=split(/ :: /, $temp_contents[$i]);
    ($ID2, $name2, $age2, $sex2, $location2, $pref_sex2, $prefer2)=split(/ :: /, $temp_contents[$j]);
    if ($age > $age2) {
      $temp_temp=$temp_contents[$j];
      $temp_contents[$j]=$temp_contents[$i];
      $temp_contents[$i]=$temp_temp;
    }
  }
}

@temp_contents = reverse (@temp_contents);


print <<EndOfHTML;
Click on a name to see more information on that particular pen pal.<br>
Viewing $total entries.<br>
<table align="center">
<tr><th bgcolor=#ffffff><font color="#000000">Name</th></font>
    <th bgcolor=#ffffff><font color="#000000">Age</th></font>
    <th bgcolor=#ffffff><font color="#000000">Sex</td></font>
    <th bgcolor=#ffffff><font color="#000000">Location</th></font>
    <th bgcolor=#ffffff><font color="#000000">Prefered Pen Pal</th></font>
    <th bgcolor=#ffffff><font color="#000000">Prefer Writing By</font></th>
</tr>
EndOfHTML


foreach $line (@temp_contents) {
  ($ID, $name, $age, $sex, $location, $pref_sex, $prefer)=split(/ :: /, $line);


print <<EndOfHTML;

<tr>
<td><a href="view.cgi?pal_num=$ID">$name</a></td>
<td>$age</td>
<td>$sex</td>
<td>$location</td>
<td align=center>$pref_sex</td>
<td align=center>$prefer</td>
</tr>


EndOfHTML

}

print ("</table>");

print <<EndOfHTML;
<p>
<hr>
<center>
<a href="../">Home</a><br>
View Pen Pal Users:
<a href="list.cgi?view=all">All</a> |
<a href="list.cgi?view=female">Female</a> |
<a href="list.cgi?view=male">Male</a> |<br>
<a href="../add.html">Add Entry</a>
</center>
      </tr>
    </table>
    </td>
  </tr>
  <tr>
    <td valign="top" colspan="2" height="30"><hr noshade size="1" color="#FFFFFF" width="73%"
    align="right">
    <p align="center"><font face="arial" size="2">Copyright NIS ©1998-99. All rights
    reserved.</font></td>
  </tr>
</table>
</center></div>
</body>
</html>
EndOfHTML

