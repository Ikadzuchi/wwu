#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� LIGHT BOARD - admin.cgi (2004/01/31)
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# �O���t�@�C����荞��
require './jcode.pl';
require './init.cgi';

&decode;
&setfile;
if ($mode eq "admin") { &admin; }
elsif ($mode eq "setup") { &setup; }
&enter;

#-------------------------------------------------
#  �Ǘ����[�h
#-------------------------------------------------
sub admin {
	# ���O�C�����
	if ($in{'pass'} eq "") {
		&header;
		print "<div align='center'>\n";
		print "<h4>�p�X���[�h����͂��Ă�������</h3>\n";
		print "<form action=\"$admin\" method=POST>\n";
		print "<input type=radio name=mode value=admin checked>�L��\n";
		print "<input type=radio name=mode value=setup>�ݒ�<br><br>\n";
		print "<input type=password name=pass size=8>\n";
		print "<input type=submit value=' �F�� '></form></div>\n";
		print "</body></html>\n";
		exit;
	# �F��
	} elsif ($in{'pass'} ne $pass) {
		&error("�p�X���[�h���Ⴂ�܂�");
	}

	# �폜
	if ($in{'job'} eq "del" && $in{'no'}) {

		# ���b�N�J�n
		&lock if ($lockkey);

		# �폜�L���������
		@new=();
		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no) = split(/<>/);
			next if ($in{'no'} == $no);
			push(@new,$_);
		}
		close(IN);

		# �X�V
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ���b�N����
		&unlock if ($lockkey);

	# �C���t�H�[��
	} elsif ($in{'job'} eq "edit" && $in{'no'}) {

		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);
			last if ($in{'no'} == $no);
		}
		close(IN);

		&edit_form($no,$dat,$nam,$eml,$sub,$com,$url);

	# �C�����s
	} elsif ($in{'job'} eq "edit2") {

		# ���̓`�F�b�N
		if ($in{'url'} eq "http://") { $in{'url'}=""; }

		# ���b�N�J�n
		&lock if ($lockkey);

		# �폜�L���������
		@new=();
		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,$tim) = split(/<>/);
			if ($in{'no'} == $no) {
				$_="$no<>$dat<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$hos<>$pwd<>$tim<>\n";
			}
			push(@new,$_);
		}
		close(IN);

		# �X�V
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ���b�N����
		&unlock if ($lockkey);
	}

	# �Ǘ����
	&header;
	print <<"EOM";
[<a href="$script?">�f���ɖ߂�</a>]
<h3>�L�������e�i���X</h3>
<form action="$admin" method="POST">
<input type=hidden name=mode value="admin">
<input type=hidden name=pass value="$in{'pass'}">
<select name=job>
<option value="edit">�C��
<option value="del">�폜</select>
<input type=submit value="���M����">
<DL>
EOM

	# �L���W�J
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);
		$nam = "<a href=\"mailto:$eml\">$nam</a>" if ($eml);
		$com =~ s/<([^>]|\n)*>//g;
		if (length($com) > 70) {
			$com = substr($com,0,70);
			$com .= "...";
		}

		print "<DT><hr><input type=radio name=no value=\"$no\">";
		print "[<b>$no</b>] <b style='color:$subcol'>$sub</b> - <b>$nam</b> ";
		print "- $dat<DD>$com <font color=\"$subcol\">&lt;$hos&gt;</font>\n";
	}
	close(IN);

	print "<DT><hr></DL></form>\n</body></html>\n";
	exit;
}

#-------------------------------------------------
#  �ݒ菈��
#-------------------------------------------------
sub setup {
	if ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# �ҏW���s
	if ($in{'job'} eq "setup") {

		# �`�F�b�N
		if (!$in{'home'}) { &error('�߂��̓��͂�����܂���'); }
		if (!$in{'max'}) { &error('�ő�L�����̓��͂�����܂���'); }
		if (!$in{'plog'}) { &error('�\�������̓��͂�����܂���'); }
		if (!$in{'b_size'}) { &error('�{�������T�C�Y�̓��͂�����܂���'); }
		if ($in{'t_img'} eq "http://") { $in{'t_img'}=""; }
		if ($in{'bg'} eq "http://") { $in{'bg'}=""; }

		# �X�V
		open(OUT,">$setfile") || &error("Write Error : $setfile");
		print OUT "$in{'title'}<>$in{'t_col'}<>$in{'t_size'}<>$in{'t_face'}<>$in{'t_img'}<>$in{'bg'}<>$in{'bc'}<>$in{'tx'}<>$in{'li'}<>$in{'vl'}<>$in{'al'}<>$in{'home'}<>$in{'max'}<>$in{'subcol'}<>$in{'refcol'}<>$in{'plog'}<>$in{'b_size'}<>$in{'mail'}<>$in{'deny'}<>$in{'link'}<>$in{'wait'}<>";
		close(OUT);

		# �������b�Z�[�W
		&header;
		print "<div align=center><h3>�ݒ肪�������܂���</h3>\n";
		print "<form action=\"$script\">\n";
		print "<input type=submit value='�f���ɖ߂�'></form>\n";
		print "</body></html>\n";
		exit;
	}

	&header;

	$t_img ||= "http://";
	$bg    ||= "http://";
	$home  ||= "http://";
	$b_size =~ s/\D//g;

	print <<"EOM";
[<a href="$script?">�f���ɖ߂�</a>]
<h3>�ݒ���</h3>
<UL>
<LI>�C�����镔���̂ݕύX���Ă��������B
<form action="$admin" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="setup">
<input type=hidden name=job value="setup">
<table border=0>
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>�^�C�g����</td>
  <td><input type=text name=title size=30 value="$title"></td>
</tr>
<tr>
  <td>�^�C�g���F</td>
  <td><input type=text name=t_col size=12 value="$t_col">
	<font color="$t_col">��</font></td>
</tr>
<tr>
  <td>�^�C�g���T�C�Y</td>
  <td><input type=text name=t_size size=5 value="$t_size"> �s�N�Z��</td>
</tr>
<tr>
  <td>�^�C�g���t�H���g</td>
  <td><input type=text name=t_face size=30 value="$t_face"></td>
</tr>
<tr>
  <td>�^�C�g���摜</td>
  <td><input type=text name=t_img size=40 value="$t_img"> �i�C�Ӂj</td>
</tr>
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>�ǎ�</td>
  <td><input type=text name=bg size=40 value="$bg"> �i�C�Ӂj</td>
</tr>
<tr>
  <td>�w�i�F</td>
  <td><input type=text name=bc size=12 value="$bc">
	<font color="$bc">��</font></td>
</tr>
<tr>
  <td>�����F</td>
  <td><input type=text name=tx size=12 value="$tx">
	<font color="$tx">��</font></td>
</tr>
<tr>
  <td>�����N�F</td>
  <td><input type=text name=li size=12 value="$li">
	<font color="$li">��</font> �i���K��j</td>
</tr>
<tr>
  <td>�����N�F</td>
  <td><input type=text name=vl size=12 value="$vl">
	<font color="$vl">��</font> �i�K��ρj</td>
</tr>
<tr>
  <td>�����N�F</td>
  <td><input type=text name=al size=12 value="$al">
	<font color="$al">��</font> �i�K�⒆�j</td>
</tr>
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>�L���薼�F</td>
  <td><input type=text name=subcol size=12 value="$subcol">
	<font color="$subcol">��</font></td>
</tr>
<tr>
  <td>���p���F</td>
  <td><input type=text name=refcol size=12 value="$refcol">
	<font color="$refcol">��</font></td>
</tr>
<tr>
  <td>�߂��</td>
  <td><input type=text name=home size=40 value="$home"></td>
</tr>
<tr>
  <td>�ő�L����</td>
  <td><input type=text name=max size=5 value="$max"></td>
</tr>
<tr>
  <td>�\\������</td>
  <td><input type=text name=plog size=5 value="$plog">
	�i1�y�[�W����̋L���\\�����j</td>
</tr>
<tr>
  <td>�{������</td>
  <td><input type=text name=b_size size=5 value="$b_size"> �s�N�Z��</td>
</tr>
<tr>
  <td>URL�����N</td>
  <td>
EOM
	if ($link) {
		print "<input type=radio name=link value=1 checked>����\n",
		"<input type=radio name=link value=0>���Ȃ�\n";
	} else {
		print "<input type=radio name=link value=1>����\n",
		"<input type=radio name=link value=0 checked>���Ȃ�\n";
	}
	print "&nbsp;&nbsp;�i�L������URL�����������N�j</td></tr>\n";
	print "<tr><td>���e�Ԋu</td><td>";
	print "<input type=text name=wait size=5 value=\"$wait\"> �b &nbsp; ";
	print "�i����z�X�g�̘A�����e����j</td></tr>\n";

	if ($sendmail) {
		print "<tr><td colspan=2><hr></td></tr>\n";
		print "<tr><td>�d���[��</td>";
		print "<td><input type=text name=mail size=30 value=\"$mail\"><br>\n";
		print "�i���[���ʒm����ꍇ�j</td></tr>\n";
	}

	print <<"EOM";
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>���ۃz�X�g</td>
  <td><input type=text name=deny size=40 value="$deny"><br>
	�i�A�N�Z�X���ۂ���z�X�g�����X�y�[�X�ŋ�؂�j</td>
</tr>
<tr><td colspan=2><hr></td></tr>
</table>
<input type=submit value="��L�ݒ���C������"></form>
</body>
</html>
EOM
	exit;
}


__END__

