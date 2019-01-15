#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� LIGHT BOARD - light.cgi (2004/01/31)
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# �O���t�@�C����荞��
require './jcode.pl';
require './init.cgi';

&decode;
&setfile;
if ($mode eq "regist") { &regist; }
elsif ($mode eq "howto") { &howto; }
elsif ($mode eq "find") { &find; }
elsif ($mode eq "dellog") { &dellog; }
elsif ($mode eq "editlog") { &editlog; }
elsif ($mode eq "past" && $pastkey) { &pastlog; }
elsif ($mode eq "check") { &check; }
&viewlog;

#-------------------------------------------------
#  �L���\��
#-------------------------------------------------
sub viewlog {
	local($x,$y,$i,$flag,$no,$dat,$nam,$eml,$sub,$com,$url,$resub,$recom,$nexr,$back);

	# �N�b�L�[�擾
	local($cnam,$ceml,$curl,$cpwd) = &get_cookie;
	$curl ||= "http://";

	# �^�C�g���\��
	&header;
	print "<div align=\"center\">\n";
	if ($t_img) {
		print "<img src=\"$t_img\" alt=\"$title\">\n";
	} else {
		print "<b style=\"color:$t_col; font-size:$t_size",
		"px; font-family:'$t_face'\">$title</b>\n";
	}

	# �\���J�n
	print <<"EOM";
<hr width="90%">
[<a href="$home" target="_top">�g�b�v�ɖ߂�</a>]
[<a href="$script?mode=howto">���ӎ���</a>]
[<a href="$script?mode=find">���[�h����</a>]
EOM

	# �ߋ����O�����N
	print "[<a href=\"$script?mode=past\">�ߋ����O</a>]\n" if ($pastkey);

	# ���O�ҏW�@�\�̃����N
	print "[<a href=\"$admin?mode=admin\">�Ǘ��p</a>]\n";

	# �ԐM���[�h
	$resub='';
	$recom='';
	if ($in{'res'}) {
		# ���p�L�����o
		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com) = split(/<>/);
			last if ($in{'res'} == $no);
		}
		close(IN);

		# �R�����g�Ɉ��p���t��
		$recom = "&gt; $com";
		$recom =~ s/<br>/\n&gt; /g;

		# �薼�Ɉ��p���ڕt��
		$sub =~ s/^Re://;
		$resub = "Re:[$in{'res'}] $sub";
	}

	# ���e�t�H�[��
	print <<"EOM";
<hr width="90%"></div>
<form method="POST" action="$script">
<input type=hidden name=mode value="regist">
<blockquote>
<table cellpadding=1 cellspacing=1>
<tr>
  <td><b>���Ȃ܂�</b></td>
  <td><input type=text name=name size=28 value="$cnam"></td>
</tr>
<tr>
  <td><b>�d���[��</b></td>
  <td><input type=text name=email size=28 value="$ceml"></td>
</tr>
<tr>
  <td><b>�^�C�g��</b></td>
  <td><input type=text name=sub size=36 value="$resub">
	<input type=submit value="���e����"><input type=reset value="���Z�b�g"></td>
</tr>
<tr>
  <td colspan=2><b>�R�����g</b><br>
  <textarea cols=56 rows=7 name=comment wrap="soft">$recom</textarea></td>
</tr>
<tr>
  <td><b>�Q�Ɛ�</b></td>
  <td><input type=text size=50 name=url value="$curl"></td>
</tr>
<tr>
  <td><b>�Ï؃L�[</b></td>
  <td><input type=password name=pwd size=8 maxlength=8 value="$cpwd">
  �i�L�������e�p�j</td>
</tr>
</table>
</form>
</blockquote>
<dl>
EOM

	# �L���W�J
	$i=0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $plog) { next; }

		($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);
		$nam = "<a href=\"mailto:$eml\">$nam</a>" if ($eml);
		&auto_link($com) if ($link);
		$com =~ s/([>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;
		$com .= "<p><a href=\"$url\" target=\"_blank\">$url</a>" if ($url);

		# �L���ҏW
		print "<dt><hr><table><tr><td valign=top>[<b>$no</b>] ";
		print "<b style=\"color:$subcol\">$sub</b> ���e�ҁF<b>$nam</b> ";
		print "���e���F$dat &nbsp;</td><td valign=top>";
		print "<form action=\"$script\">\n";
		print "<input type=hidden name=res value=\"$no\">\n";
		print "<input type=submit value='�ԐM'></td></form></tr></table><br>\n";
		print "<dd>$com<br><br>\n";
	}
	close(IN);

	print "<dt><hr></dl>\n";

	$next = $page + $plog;
	$back = $page - $plog;

	$flag=0;
	print "<p><table><tr>\n";
	if ($back >= 0) {
		$flag=1;
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=page value=\"$back\">\n";
		print "<input type=submit value=\"�O�y�[�W\"></td></form>\n";
	}
	if ($next < $i) {
		$flag=1;
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=page value=\"$next\">\n";
		print "<input type=submit value=\"���y�[�W\"></td></form>\n";
	}

	# �y�[�W�ړ��{�^���\��
	if ($flag) {
		print "<td width=10></td><td class=num>";
		$x=1;
		$y=0;
		while ($i > 0) {
			if ($page == $y) { print "<b>[$x]</b>\n"; }
			else { print "[<a href=\"$script?page=$y\">$x</a>]\n"; }
			$x++;
			$y += $plog;
			$i -= $plog;
		}
		print "</td>";
	}
	print <<"EOM";
</tr></table>
<div align="center">
<form action="$script" method="POST">
���� <select name=mode>
<option value=editlog>�C��
<option value=dellog>�폜</select>
�L��No<input type=text name=no size=3>
�Ï؃L�[<input type=password name=pwd size=6 maxlength=8>
<input type=submit value="���M"></form>
<!-- ���쌠�\\�L:�폜�֎~($ver) -->
<span style="font-size:10px;font-family:Verdana,Helvetica">
- <a href="http://www.kent-web.com/" target="_top">LightBoard</a> -
</span></div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ���e��t
#-------------------------------------------------
sub regist {
	local($pwd,$past,@w,@past,@file);

	# ���̓`�F�b�N
	if (!$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }
	if ($in{'name'} eq "") { &error("���O�����͂���Ă��܂���"); }
	if ($in{'comment'} eq "") { &error("�R�����g�����͂���Ă��܂���"); }
	if ($in{'email'} && $in{'email'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
		&error("�d���[���̓��͓��e������������܂���");
	}
	if ($in{'url'} eq "http://") { $in{'url'}=""; }
	if ($in{'sub'} eq "") { $in{'sub'} = "����"; }

	# �t�@�C�����b�N
	&lock if ($lockkey);

	# ���O���J��
	open(IN,"$logfile") || &error("Open Error: $logfile");
	@file = <IN>;
	close(IN);

	# ��d���e�֎~
	local($no,$dat,$nam,$eml,$sub,$com,$url,$ho,$pw,$tim) = split(/<>/, $file[0]);
	if ($host eq $ho && $wait > time - $tim) {
		&error("�A�����e�͂������΂炭���Ԃ�u���Ă�������");
	}
	if ($in{'name'} eq $nam && $in{'comment'} eq $com) {
		&error("��d���e�͋֎~�ł�");
	}

	# �L��������
	@past=();
	while ($max <= @file) {
		$past = pop(@file);
		unshift(@past,$past) if ($pastkey);
	}

	# �ߋ����O
	if (@past > 0) { &past_make(@past); }

	# �폜�L�[���Í���
	if ($in{'pwd'} ne "") { $pwd = &encrypt($in{'pwd'}); }

	# ���Ԃ��擾
	local($min,$hour,$mday,$mon,$year,$wday) = (localtime(time))[1..6];
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$w[$wday],$hour,$min);

	# ���O���X�V
	$time = time;
	$no++;
	unshift (@file,"$no<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$time<>\n");
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @file;
	close(OUT);

	# ���b�N����
	&unlock if ($lockkey);

	# �N�b�L�[�𔭍s
	&set_cookie($in{'name'},$in{'email'},$in{'url'},$in{'pwd'},);

	# ���[������
	if ($sendmail && $mail && $in{'email'} ne $mail) { &mailto; }

	# �������b�Z�[�W
	&header;
	print "<div align=center><hr width=400>\n";
	print "<h3>���e�͐���ɏ�������܂���</h3>\n";
	print "<form action=\"$script\">\n";
	print "<input type=submit value='�f���֖߂�'></form>\n";
	print "<hr width=400></div>\n</body></html>\n";
	exit;
}

#-------------------------------------------------
#  ���ӎ���
#-------------------------------------------------
sub howto {
	&header;
	print <<EOM;
<div align="center">
<table border=1 width="85%" cellpadding=15>
<tr><td class="r">
<h3>�f�����p��̒���</h3>
<ol>
<li>���̌f����<b>�N�b�L�[�Ή�</b>�ł��B1�x�L���𓊍e���������ƁA���Ȃ܂��A�d���[���A�t�q�k�A�Ï؃L�[�̏���2��ڈȍ~�͎������͂���܂��B�i���������p�҂̃u���E�U���N�b�L�[�Ή��̏ꍇ�j
<li>���e���e�ɂ́A<b>�^�O�͈�؎g�p�ł��܂���B</b>
<li>�L���𓊍e�����ł̕K�{���͍��ڂ�<b>�u���Ȃ܂��v</b>��<b>�u���b�Z�[�W�v</b>�ł��B�d���[���A�t�q�k�A�薼�A�Ï؃L�[�͔C�ӂł��B
<li>�L���ɂ́A<b>���p�J�i�͈�؎g�p���Ȃ��ŉ������B</b>���������̌����ƂȂ�܂��B
<li>�L���̓��e����<b>�Ï؃L�[</b>�i�p������8�����ȓ��j�����Ă����ƁA���̋L���͎���Ï؃L�[�ɂ���č폜���邱�Ƃ��ł��܂��B
<li>�L���̕ێ������͍ő�<b>$max��</b>�ł��B����𒴂���ƌÂ����Ɏ����폜����܂��B
<li>�����̋L���ɊȒP��<b>�u�ԐM�v</b>���邱�Ƃ��ł��܂��B�e�L���ɂ���<b>�u�ԐM�v�{�^��</b>�������Ɠ��e�t�H�[�����ԐM�p�ƂȂ�܂��B
<li>�ߋ��̓��e�L������<b>�u�L�[���[�h�v�ɂ���ĊȈՌ������ł��܂��B</b>�g�b�v���j���[��<a href="$script?mode=find">�u���[�h�����v</a>�̃����N���N���b�N����ƌ������[�h�ƂȂ�܂��B
<li>�Ǘ��҂��������s���v�Ɣ��f����L���⑼�l���排�������L���͗\\���Ȃ��폜���邱�Ƃ�����܂��B
</ol>
</td></tr></table>
<form>
<input type=button value="�f���ɖ߂�" onClick="history.back()">
</form>
</div>
</body>
</html>
EOM

	exit;
}

#-------------------------------------------------
#  �������
#-------------------------------------------------
sub find {
	&header;
	print <<"EOM";
<form action="$script">
<input type=submit value="�f���ɖ߂�"></form>
<ul>
<li>����������<b>�L�[���[�h</b>����͂��A�u�����v�u�\\���v��I�����āu�����v�{�^���������ĉ������B
<li>�L�[���[�h�͔��p�X�y�[�X�ŋ�؂��ĕ����w�肷�邱�Ƃ��ł��܂��B
</ul>
<table><tr>
EOM
	&search("find", $logfile);
	print "</body></html>\n";
	exit;
}

#-------------------------------------------------
#  ��������
#-------------------------------------------------
sub search {
	local($md, $target) = @_;
	local($i, $flag, $next, $back, $enwd, $wd, @wd);

	print "<td><form action=\"$script\" method=\"POST\">\n";
	print "<input type=hidden name=mode value=\"$md\">\n";

	local($para)='';
	if ($md eq "past") {
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		$para = "&pastlog=$in{'pastlog'}";
	}

	print "�L�[���[�h <input type=text name=word size=35 value=\"$in{'word'}\"> ";
	print "���� <select name=cond> &nbsp; ";

	if ($in{'cond'} eq "") { $in{'cond'} = "AND"; }
	foreach ("AND", "OR") {
		if ($in{'cond'} eq $_) {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select> �\\�� <select name=view>\n";
	if ($in{'view'} eq "") { $in{'view'} = 10; }
	foreach (10,15,20,25,30) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected>$_��\n";
		} else {
			print "<option value=\"$_\">$_��\n";
		}
	}
	print "</select> <input type=submit value=' ���� '>";
	print "</td></form></tr></table>\n";

	# ���[�h�����̎��s�ƌ��ʕ\��
	if ($in{'word'} ne "") {

		# ���͓��e�𐮗�
		$in{'word'} =~ s/\x81\x40/ /g;
		@wd = split(/\s+/, $in{'word'});

		# �t�@�C����ǂݍ���
		print "<dl>\n";
		$i=0;
		open(IN,"$target") || &error("Open Error: $target");
		while (<IN>) {
			$flag=0;
			foreach $wd (@wd) {
				if (index($_,$wd) >= 0) {
					$flag=1;
					if ($in{'cond'} eq 'OR') { last; }
				} else {
					if ($in{'cond'} eq 'AND') { $flag=0; last; }
				}
			}
			if ($flag) {
				$i++;
				if ($i < $page + 1) { next; }
				if ($i > $page + $in{'view'}) { next; }

				($no,$ymd,$nam,$eml,$sub,$com,$url) = split(/<>/);
				if ($eml) { $nam="<a href=\"mailto:$eml\">$nam</a>"; }
				if ($url) { $com .= "<P><a href=\"$url\" target=\"_blank\">$url</a>"; }

				print "<dt><hr>[<b>$no</b>] <b style='color:$subcol'>$sub</b> ";
				print "���e�ҁF<b>$nam</b> ���e���F$ymd<br><br>\n";
				print "<dd>$com<br><br>\n";
			}
		}
		close(IN);
		print "<dt><hr>�������ʁF<b>$i</b>��</dl>\n";

		$next = $page + $in{'view'};
		$back = $page - $in{'view'};
		$enwd = &url_enc($in{'word'});
		if ($back >= 0) {
			print "[<a href=\"$script?mode=$md&page=$back&word=$enwd&view=$in{'view'}&cond=$in{'cond'}$para\">�O��$in{'view'}��</a>]\n";
		}
		if ($next < $i) {
			print "[<a href=\"$script?mode=$md&page=$next&word=$enwd&view=$in{'view'}&cond=$in{'cond'}$para\">����$in{'view'}��</a>]\n";
		}
		print "</body></html>\n";
		exit;
	}
}

#-------------------------------------------------
#  �N�b�L�[���s
#-------------------------------------------------
sub set_cookie {
	local(@cook) = @_;
	local($gmt, $cook, @t, @m, @w);

	@t = gmtime(time + 60*24*60*60);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# ���ەW�������`
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# �ۑ��f�[�^��URL�G���R�[�h
	foreach (@cook) {
		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cook .= "$_<>";
	}

	# �i�[
	print "Set-Cookie: LIGHT_BOARD=$cook; expires=$gmt\n";
}

#-------------------------------------------------
#  �N�b�L�[�擾
#-------------------------------------------------
sub get_cookie {
	local($key, $val, *cook);

	# �N�b�L�[���擾
	$cook = $ENV{'HTTP_COOKIE'};

	# �Y��ID�����o��
	foreach ( split(/;/, $cook) ) {
		($key, $val) = split(/=/);
		$key =~ s/\s//g;
		$cook{$key} = $val;
	}

	# �f�[�^��URL�f�R�[�h���ĕ���
	foreach ( split(/<>/, $cook{'LIGHT_BOARD'}) ) {
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;

		push(@cook,$_);
	}
	return (@cook);
}

#-------------------------------------------------
#  �L���폜
#-------------------------------------------------
sub dellog {
	local($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,@new);

	# ���̓`�F�b�N
	if (!$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }
	if ($in{'no'} eq "" || $in{'pwd'} eq "") {
		&error("�L��No���̓p�X���[�h�����͂���Ă��܂���");
	}

	# ���b�N�J�n
	&lock if ($lockkey);

	# ���O��ǂݍ���
	$flag=0;
	@new=();
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);
		if ($in{'no'} == $no) {
			if ($pwd eq "") { $flag=2; last; }
			$check = &decrypt($in{'pwd'}, $pwd);
			if ($check) { $flag=1; next; }
			else { $flag=3; last; }
		}
		push(@new,$_);
	}
	close(IN);
	if (!$flag) { &error("�Y���L������������܂���"); }
	elsif ($flag == 2) { &error("�p�X���[�h���ݒ肳��Ă��܂���"); }
	elsif ($flag == 3) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# ���O�X�V
	open(OUT,">$logfile") || &error("Write Error: $logfile");
	print OUT @new;
	close(OUT);

	# ���b�N����
	&unlock if ($lockkey);

	# �������b�Z�[�W
	&header;
	print <<"EOM";
<div align="center">
<h3>�L���͐���ɍ폜����܂���</h3>
<form action="$script">
<input type=submit value="�f���ɖ߂�"></form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �L���C��
#-------------------------------------------------
sub editlog {
	local($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,@new);

	# ���̓`�F�b�N
	if ($in{'no'} eq "" || $in{'pwd'} eq "") {
		&error("�L��No���̓p�X���[�h�����͂���Ă��܂���");
	}

	# �C�����s
	if ($in{'job'} eq "edit2") {
		# ���̓`�F�b�N
		if ($in{'name'} eq "") { &error("���O�����͂���Ă��܂���"); }
		if ($in{'comment'} eq "") { &error("�R�����g�����͂���Ă��܂���"); }
		if ($in{'email'} && $in{'email'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,5}$/) {
			&error("�d���[���̓��͓��e������������܂���");
		}
		if ($in{'url'} eq "http://") { $in{'url'}=""; }
		if ($in{'sub'} eq "") { $in{'sub'} = "����"; }

		# ���b�N�J�n
		&lock if ($lockkey);

		# �����ւ�
		@new=();
		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,$tim) = split(/<>/);
			if ($in{'no'} == $no) {
				$_="$no<>$dat<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$hos<>$pwd<>$tim<>\n";
				$pwd2 = $pwd;
			}
			push(@new,$_);
		}
		close(IN);

		# �F�؃`�F�b�N
		$check = &decrypt($in{'pwd'}, $pwd2);
		if (!$check) { &error("�p�X���[�h���Ⴂ�܂�"); }

		# �X�V
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ���b�N����
		&unlock if ($lockkey);

		return;
	}

	# �L�����o
	$flag=0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);
		if ($in{'no'} == $no) { $flag=1; last; }
	}
	close(IN);

	if (!$flag) {
		&error("�Y���̋L����������܂���");
	} elsif ($pwd eq "") {
		&error('���̋L���̓p�X���[�h���ݒ肳��Ă��Ȃ����߁A�C���s�\�ł�');
	}
	$check = &decrypt($in{'pwd'}, $pwd);
	if (!$check) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# �C���t�H�[��
	&edit_form($no,$dat,$nam,$eml,$sub,$com,$url);
}

#-------------------------------------------------
#  ���[�����M
#-------------------------------------------------
sub mailto {
	local($msub,$mbody,$email,$com);

	# �L���̉��s�E�^�O�𕜌�
	$com  = $in{'comment'};
	$com =~ s/<br>/\n/g;
	$com =~ s/&lt;/</g;
	$com =~ s/&gt;/>/g;
	$com =~ s/&quot;/"/g;
	$com =~ s/&amp;/&/g;

	# ���[���{�����`
	$mbody = <<"EOM";
���e�����F$date
�z�X�g���F$host
�u���E�U�F$ENV{'HTTP_USER_AGENT'}

���e�Җ��F$in{'name'}
�d���[���F$in{'email'}
�t�q�k  �F$in{'url'}
�^�C�g���F$in{'sub'}

$com
EOM

	# �薼��BASE64��
	$msub = &base64("[$title : $no] $in{'sub'}");

	# ���[���A�h���X���Ȃ��ꍇ
	if ($in{'email'} eq "") { $email = $mail; }
	else { $email = $in{'email'}; }

	open(MAIL,"| $sendmail -t") || &error("���[�����M���s");
	print MAIL "To: $mail\n";
	print MAIL "From: $email\n";
	print MAIL "Subject: $msub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	foreach ( split(/\n/, $mbody) ) {
		&jcode'convert(*_, 'jis', 'sjis');
		print MAIL $_, "\n";
	}
	close(MAIL);
}

#-------------------------------------------------
#  BASE64�ϊ�
#-------------------------------------------------
#	�Ƃقق�WWW����Ō��J����Ă��郋�[�`�����Q�l�ɂ��܂����B
#	( http://tohoho.wakusei.ne.jp/ )
sub base64 {
	local($sub) = @_;
	&jcode'convert(*sub, 'jis', 'sjis');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	local($ch)="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	local($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ($i=0; $y=substr($x,$i,6); $i+=6) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}

#-------------------------------------------------
#  �p�X���[�h�Í�
#-------------------------------------------------
sub encrypt {
	local($inp) = $_[0];
	local($salt, $crypt, @char);

	# ��╶������`
	@char = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');

	# �����Ŏ�𒊏o
	srand;
	$salt = $char[int(rand(@char))] . $char[int(rand(@char))];

	# �Í���
	$crypt = crypt($inp, $salt) || crypt ($inp, '$1$' . $salt);
	$crypt;
}

#-------------------------------------------------
#  �p�X���[�h�ƍ�
#-------------------------------------------------
sub decrypt {
	local($inp, $log) = @_;

	# �풊�o
	local($salt) = $log =~ /^\$1\$(.*)\$/ && $1 || substr($log, 0, 2);

	# �ƍ�
	if (crypt($inp, $salt) eq $log || crypt($inp, '$1$' . $salt) eq $log) {
		return (1);
	} else {
		return (0);
	}
}

#-------------------------------------------------
#  ���������N
#-------------------------------------------------
sub auto_link {
	$_[0] =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"$2\" target=\"_top\">$2<\/a>/g;
}

#-------------------------------------------------
#  URL�G���R�[�h
#-------------------------------------------------
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#-------------------------------------------------
#  �ߋ����O���
#-------------------------------------------------
sub pastlog {
	local($no,$i,$file,$next,$back);

	open(IN,"$pastno") || &error("Open Error: $pastno");
	$no = <IN>;
	close(IN);

	$in{'pastlog'} =~ s/\D//g;
	if (!$in{'pastlog'}) { $in{'pastlog'} = $no; }

	&header;
	print <<"EOM";
[<a href="$script?">�f���ɖ߂�</a>]<hr>
<form action="$script" method="POST">
<input type=hidden name=mode value=past>
<table><tr><td><b>�ߋ����O</b> <select name=pastlog>
EOM

	# �ߋ����O�I��
	for ($i=$no; $i>0; --$i) {
		$i = sprintf("%04d", $i);
		next unless (-e "$pastdir$i\.cgi");
		if ($in{'pastlog'} == $i) {
			print "<option value=\"$i\" selected>$i\n";
		} else {
			print "<option value=\"$i\">$i\n";
		}
	}
	print "</select> <input type=submit value='�ړ�'>";
	print "</td></form><td width=20></td>\n";

	$file = sprintf("%s%04d\.cgi", $pastdir,$in{'pastlog'});
	&search("past", $file);

	print "<dl>\n";
	$i=0;
	open(IN,"$file") || &error("Open Error: $file");
	while (<IN>) {
		($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);
		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $plog) { last; }

		&auto_link($com) if ($link);
		$com =~ s/([>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;

		if ($eml) { $nam = "<a href=\"mailto:$eml\">$nam</a>"; }
		if ($url) { $url = "&lt;<a href=\"$url\" target=\"_blank\">URL</a>&gt;"; }

		print "<dt><hr>[<b>$no</b>] <b style='color:$subcol'>$sub</b> ";
		print "���e�ҁF<b>$nam</b> ���e���F$dat &nbsp; $url <br><br><dd>$com<br><br>\n";

	}
	close(IN);

	print "<dt><hr></dl>\n";

	$next = $page + $plog;
	$back = $page - $plog;

	print "<table><tr>\n";
	if ($back >= 0) {
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=past>\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		print "<input type=hidden name=page value=\"$back\">\n";
		print "<input type=submit value=\"�O��$plog��\"></td></form>\n";
	}
	if ($next < $i) {
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=past>\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		print "<input type=hidden name=page value=\"$next\">\n";
		print "<input type=submit value=\"����$plog��\"></td></form>\n";
	}
	print "</tr></table>\n</body></html>\n";
	exit;
}

#-------------------------------------------------
#  �ߋ����O����
#-------------------------------------------------
sub past_make {
	local(@past) = @_;
	local($count,$pastfile,$i,$f,@data);

	# �ߋ����O�t�@�C�������`
	open(NO,"$pastno") || &error("Open Error: $pastno");
	$count = <NO>;
	close(NO);
	$pastfile = sprintf("%s%04d\.cgi", $pastdir,$count);

	# �ߋ����O���J��
	$i=0; $f=0;
	@data=();
	open(IN,"$pastfile") || &error("Open Error: $pastfile");
	while (<IN>) {
		$i++;
		push(@data,$_);

		# �ő匏���𒴂���ƒ��f
		if ($i >= $pastmax) { $f++; last; }
	}
	close(IN);

	# �ő匏�����I�[�o�[����Ǝ��t�@�C������������
	if ($f) {
		# �J�E���g�t�@�C���X�V
		$count++;
		open(NO,">$pastno") || &error("Write Error: $pastno");
		print NO $count;
		close(NO);

		$pastfile = sprintf("%s%04d\.cgi", $pastdir,$count);
		@data = @past;
	} else {
		unshift(@data,@past);
	}

	# �ߋ����O���X�V
	open(OUT,">$pastfile") || &error("Write Error: $pastfile");
	print OUT @data;
	close(OUT);

	if ($f) { chmod(0666, $pastfile); }
}

#-------------------------------------------------
#  �`�F�b�N���[�h
#-------------------------------------------------
sub check {
	&header;
	print <<EOM;
<h2>Check Mode</h2>
<ul>
EOM

	# ���O�`�F�b�N
	foreach ($logfile, $setfile) {
		if (-e $_) {
			print "<li>�p�X�F$_ �� OK\n";
			if (-r $_ && -w $_) { print "<li>�p�[�~�b�V�����F$_ �� OK\n"; }
			else { print "�p�[�~�b�V�����F$_ �� NG\n"; }
		} else {
			print "<li>�p�X�F$_ �� NG\n";
		}
	}

	# ���b�N�f�B���N�g��
	print "<li>���b�N�`���F";
	if ($lockkey == 0) { print "���b�N�ݒ�Ȃ�\n"; }
	else {
		if ($lockkey == 1) { print "symlink\n"; }
		else { print "mkdir\n"; }
		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		print "<li>���b�N�f�B���N�g���F$lockdir\n";

		if (-d $lockdir) {
			print "<li>���b�N�f�B���N�g���̃p�X�FOK\n";
			if (-r $lockdir && -w $lockdir && -x $lockdir) {
				print "<li>���b�N�f�B���N�g���̃p�[�~�b�V�����FOK\n";
			} else {
				print "<li>���b�N�f�B���N�g���̃p�[�~�b�V�����FNG �� $lockdir\n";
			}
		} else { print "<li>���b�N�f�B���N�g���̃p�X�FNG �� $lockdir\n"; }
	}

	# �ߋ����O
	@yn = ('�Ȃ�', '����');
	print "<li>�ߋ����O�F$yn[$pastkey]\n";
	if ($pastkey) {
		if (-e $pastno) {
			print "<li>�p�X�F$pastno �� OK\n";
			if (-r $pastno && -w $pastno) {
				print "<li>�p�[�~�b�V�����F$pastno �� OK\n";
			} else {
				print "<li>�p�[�~�b�V�����F$pastno �� NG\n";
			}
		} else {
			print "<li>�p�X�F$pastno �� NG\n";
		}
		if (-d $pastdir) {
			print "<li>�p�X�F$pastdir �� OK\n";
			if (-r $pastdir && -w $pastdir && -x $pastdir) {
				print "<li>�p�[�~�b�V�����F$pastdir �� OK\n";
			} else {
				print "<li>�p�[�~�b�V�����F$pastdir �� NG\n";
			}
		} else {
			print "<li>�p�X�F$pastdir �� NG\n";
		}
	}
	print "</ul>\n</body></html>\n";
	exit;
}


__END__

