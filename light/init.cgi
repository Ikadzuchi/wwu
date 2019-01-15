#��������������������������������������������������������������������
#�� LIGHT BOARD v6.3 (2004/01/31)
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'LIGHT BOARD v6.3';
#��������������������������������������������������������������������
#��[ ���ӎ��� ]
#�� 1.���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��   �����Ȃ鑹�Q�ɑ΂��č�҂͂��̐ӔC����ؕ����܂���B
#�� 2.�ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B���[����
#��   ��鎿��ɂ͂������ł��܂���B
#��������������������������������������������������������������������
#
# [ �ݒu�� ] ���������̓p�[�~�b�V����
#
#    public_html / index.html (�z�[���y�[�W)
#       |
#       +-- bbs / light.cgi  [705]
#            |    admin.cgi  [705]
#            |    init.cgi   [604]
#            |    jcode.pl   [604]
#            |    data.cgi   [606]
#            |    light.dat  [606]
#            |    pastno.dat [606] .. �ߋ����O�p�J�E���g�t�@�C��
#            |
#            +-- lock [707] /
#            |
#            +-- past [707] / 0001.cgi [666]

#-------------------------------------------------
#  ���ݒ荀��
#-------------------------------------------------

# �X�N���v�gURL
$script = './light.cgi';

# �Ǘ��t�@�C��URL
$admin = './admin.cgi';

# ���O�t�@�C��
$logfile = './data.cgi';

# �ݒ�t�@�C��
$setfile = './light.dat';

# �Ǘ��җp�p�X���[�h(���p�p����)
$pass = 'pass';

# �t�@�C�����b�N�`��
#  �� 0=no 1=symlink�֐� 2=mkdir�֐�
$lockkey = 2;

# ���b�N�t�@�C����
$lockfile = './lock/light.lock';

# sendmail�p�X�i���[���ʒm����ꍇ�j
# �� �� /usr/lib/sendmail
$sendmail = '';

# �ߋ����O�@�\ (0=no 1=yes)
$pastkey = 0;

# �ߋ����O�f�B���N�g��
$pastdir = './past/';

# �ߋ����O�J�E���g�t�@�C��
$pastno = './pastno.dat';

# �ߋ����O�P�t�@�C������̍ő匏��
$pastmax = 400;

# �z�X�g�擾���@
# 0 : gethostbyaddr�֐����g��Ȃ�
# 1 : gethostbyaddr�֐����g��
$gethostbyaddr = 0;

#-------------------------------------------------
#  ���ݒ芮��
#-------------------------------------------------

#-------------------------------------------------
#  �t�H�[���f�R�[�h
#-------------------------------------------------
sub decode {
	local($buf,$key,$val);
	undef(%in);

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$post_flag=1;
		if ($ENV{'CONTENT_LENGTH'} > 51200) { &error("���e�ʂ��傫�����܂�"); }
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$post_flag=0;
		$buf = $ENV{'QUERY_STRING'};
	}

	foreach ( split(/&/, $buf) ) {
		($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# S-JIS�R�[�h�ϊ�
		&jcode'convert(*val, "sjis", "", "z");

		# �^�O����
#		$val =~ s/&/&amp;/g;
#		$val =~ s/"/&quot;/g;
#		$val =~ s/</&lt;/g;
#		$val =~ s/>/&gt;/g;
#		$val =~ s/\0//g;

		# ���s����
		if ($key eq "comment") {
			$val =~ s/\r\n/<br>/g;
			$val =~ s/\r/<br>/g;
			$val =~ s/\n/<br>/g;
		} else {
			$val =~ s/\r//g;
			$val =~ s/\n//g;
		}
		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	$page = $in{'page'};
	$mode = $in{'mode'};
	$headflag=0;
	$lockflag=0;
	$ENV{'TZ'} = "JST-9";
}

#-------------------------------------------------
#  �ݒ�t�@�C���F��
#-------------------------------------------------
sub setfile {
	local($flag);

	# �ݒ�t�@�C���ǂݍ���
	open(IN,"$setfile") || &error("Open Error : $setfile");
	$file = <IN>;
	close(IN);

	# �ݒ���e�F��
	($title,$t_col,$t_size,$t_face,$t_img,$bg,$bc,$tx,$li,$vl,$al,$home,$max,$subcol,$refcol,$plog,$b_size,$mail,$deny,$link,$wait) = split(/<>/, $file);

	# IP&�z�X�g�擾
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	if ($host eq "") { $host = $addr; }

	# �A�N�Z�X����
	if ($deny) {
		$flag=0;
		foreach ( split(/\s+/, $deny) ) {
			if ($host =~ /$_/i) { $flag=1; last; }
		}
		if ($flag) { &error("�����������p�ł��܂���"); }
	}

	$b_size .= "px";
}

#-------------------------------------------------
#  HTML�w�b�_
#-------------------------------------------------
sub header {
	if ($headflag) { return; }
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META HTTP-EQUIV="Content-Style-Type" content="text/css">
<STYLE TYPE="text/css">
<!--
body,tr,td,th {
	font-size:$b_size;
	font-family:"MS UI Gothic","�l�r �o�S�V�b�N",Osaka;
}
.num { font-family:Verdana,Helvetica,Arial; }
.l { background-color: #666666; color: #ffffff; }
.r { background-color: #ffffff; color: #000000; }
-->
</STYLE>
<title>$title</title></head>
EOM
	if ($bg) {
		print "<body background=\"$bg\" bgcolor=\"$bc\" text=\"$tx\" link=\"$li\" vlink=\"$vl\" alink=\"$al\">\n";
	} else {
		print "<body bgcolor=\"$bc\" text=\"$tx\" link=\"$li\" vlink=\"$vl\" alink=\"$al\">\n";
	}
	$headflag=1;
}

#-------------------------------------------------
#  �G���[����
#-------------------------------------------------
sub error {
	if ($lockflag) { &unlock; }

	&header;
	print <<"EOM";
<div align="center">
<hr width=400>
<h3>ERROR !</h3>
<font color="#dd0000">$_[0]</font>
<p>
<form>
<input type=button value="�O��ʂɖ߂�" onClick="history.back()">
</form>
<p>
<hr width=400>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ���b�N����
#-------------------------------------------------
sub lock {
	# ���g���C��
	local($retry) = 5;

	# �Â����b�N�͍폜
	if (-e $lockfile) {
		local($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 30) { &unlock; }
	}

	# symlink�֐������b�N
	if ($lockkey == 1) {
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}

	# mkdir�֐������b�N
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	}

	$lockflag=1;
}

#-------------------------------------------------
#  ���b�N����
#-------------------------------------------------
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }

	$lockflag=0;
}

#-------------------------------------------------
#  �ҏW�t�H�[��
#-------------------------------------------------
sub edit_form {
	local($no,$dat,$nam,$eml,$sub,$com,$url) = @_;
	$url ||= "http://";
	$com =~ s/<br>/\r/g;

	&header;
	print <<"EOM";
[<a href="javascript:history.back()">�O��ʂɖ߂�</a>]
<h3>�ҏW�t�H�[��</h3>
<ul>
<li>�C�����镔���̂ݕύX���Ă��������B
EOM

	if ($in{'pass'} ne "") {
		print "<form action=\"$admin\" method=\"POST\">\n";
		print "<input type=hidden name=no value=\"$in{'no'}\">\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		print "<input type=hidden name=mode value=\"admin\">\n";
		print "<input type=hidden name=job value=\"edit2\">\n";
	} else {
		print "<form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=\"editlog\">\n";
		print "<input type=hidden name=no value=\"$in{'no'}\">\n";
		print "<input type=hidden name=pwd value=\"$in{'pwd'}\">\n";
		print "<input type=hidden name=job value=\"edit2\">\n";
	}

	print <<"EOM";
���e�Җ�<br><input type=text name=name size=28 value="$nam"><br>
�d���[��<br><input type=text name=email size=28 value="$eml"><br>
�^�C�g��<br><input type=text name=sub size=36 value="$sub"><br>
�Q�Ɛ�<br><input type=text name=url size=45 value="$url"><br>
�R�����g<br><textarea name=comment cols=58 rows=7 wrap=soft>$com</textarea><br>
<input type=submit value=" �C�����s�� "></form>
</ul>
</body>
</html>
EOM
	exit;
}


1;

__END__

