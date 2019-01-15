#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ LIGHT BOARD - admin.cgi (2004/01/31)
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

# 外部ファイル取り込み
require './jcode.pl';
require './init.cgi';

&decode;
&setfile;
if ($mode eq "admin") { &admin; }
elsif ($mode eq "setup") { &setup; }
&enter;

#-------------------------------------------------
#  管理モード
#-------------------------------------------------
sub admin {
	# ログイン画面
	if ($in{'pass'} eq "") {
		&header;
		print "<div align='center'>\n";
		print "<h4>パスワードを入力してください</h3>\n";
		print "<form action=\"$admin\" method=POST>\n";
		print "<input type=radio name=mode value=admin checked>記事\n";
		print "<input type=radio name=mode value=setup>設定<br><br>\n";
		print "<input type=password name=pass size=8>\n";
		print "<input type=submit value=' 認証 '></form></div>\n";
		print "</body></html>\n";
		exit;
	# 認証
	} elsif ($in{'pass'} ne $pass) {
		&error("パスワードが違います");
	}

	# 削除
	if ($in{'job'} eq "del" && $in{'no'}) {

		# ロック開始
		&lock if ($lockkey);

		# 削除記事抜き取り
		@new=();
		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no) = split(/<>/);
			next if ($in{'no'} == $no);
			push(@new,$_);
		}
		close(IN);

		# 更新
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ロック解除
		&unlock if ($lockkey);

	# 修正フォーム
	} elsif ($in{'job'} eq "edit" && $in{'no'}) {

		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);
			last if ($in{'no'} == $no);
		}
		close(IN);

		&edit_form($no,$dat,$nam,$eml,$sub,$com,$url);

	# 修正実行
	} elsif ($in{'job'} eq "edit2") {

		# 入力チェック
		if ($in{'url'} eq "http://") { $in{'url'}=""; }

		# ロック開始
		&lock if ($lockkey);

		# 削除記事抜き取り
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

		# 更新
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ロック解除
		&unlock if ($lockkey);
	}

	# 管理画面
	&header;
	print <<"EOM";
[<a href="$script?">掲示板に戻る</a>]
<h3>記事メンテナンス</h3>
<form action="$admin" method="POST">
<input type=hidden name=mode value="admin">
<input type=hidden name=pass value="$in{'pass'}">
<select name=job>
<option value="edit">修正
<option value="del">削除</select>
<input type=submit value="送信する">
<DL>
EOM

	# 記事展開
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
#  設定処理
#-------------------------------------------------
sub setup {
	if ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	# 編集実行
	if ($in{'job'} eq "setup") {

		# チェック
		if (!$in{'home'}) { &error('戻り先の入力がありません'); }
		if (!$in{'max'}) { &error('最大記事数の入力がありません'); }
		if (!$in{'plog'}) { &error('表示件数の入力がありません'); }
		if (!$in{'b_size'}) { &error('本文文字サイズの入力がありません'); }
		if ($in{'t_img'} eq "http://") { $in{'t_img'}=""; }
		if ($in{'bg'} eq "http://") { $in{'bg'}=""; }

		# 更新
		open(OUT,">$setfile") || &error("Write Error : $setfile");
		print OUT "$in{'title'}<>$in{'t_col'}<>$in{'t_size'}<>$in{'t_face'}<>$in{'t_img'}<>$in{'bg'}<>$in{'bc'}<>$in{'tx'}<>$in{'li'}<>$in{'vl'}<>$in{'al'}<>$in{'home'}<>$in{'max'}<>$in{'subcol'}<>$in{'refcol'}<>$in{'plog'}<>$in{'b_size'}<>$in{'mail'}<>$in{'deny'}<>$in{'link'}<>$in{'wait'}<>";
		close(OUT);

		# 完了メッセージ
		&header;
		print "<div align=center><h3>設定が完了しました</h3>\n";
		print "<form action=\"$script\">\n";
		print "<input type=submit value='掲示板に戻る'></form>\n";
		print "</body></html>\n";
		exit;
	}

	&header;

	$t_img ||= "http://";
	$bg    ||= "http://";
	$home  ||= "http://";
	$b_size =~ s/\D//g;

	print <<"EOM";
[<a href="$script?">掲示板に戻る</a>]
<h3>設定画面</h3>
<UL>
<LI>修正する部分のみ変更してください。
<form action="$admin" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="setup">
<input type=hidden name=job value="setup">
<table border=0>
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>タイトル名</td>
  <td><input type=text name=title size=30 value="$title"></td>
</tr>
<tr>
  <td>タイトル色</td>
  <td><input type=text name=t_col size=12 value="$t_col">
	<font color="$t_col">■</font></td>
</tr>
<tr>
  <td>タイトルサイズ</td>
  <td><input type=text name=t_size size=5 value="$t_size"> ピクセル</td>
</tr>
<tr>
  <td>タイトルフォント</td>
  <td><input type=text name=t_face size=30 value="$t_face"></td>
</tr>
<tr>
  <td>タイトル画像</td>
  <td><input type=text name=t_img size=40 value="$t_img"> （任意）</td>
</tr>
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>壁紙</td>
  <td><input type=text name=bg size=40 value="$bg"> （任意）</td>
</tr>
<tr>
  <td>背景色</td>
  <td><input type=text name=bc size=12 value="$bc">
	<font color="$bc">■</font></td>
</tr>
<tr>
  <td>文字色</td>
  <td><input type=text name=tx size=12 value="$tx">
	<font color="$tx">■</font></td>
</tr>
<tr>
  <td>リンク色</td>
  <td><input type=text name=li size=12 value="$li">
	<font color="$li">■</font> （未訪問）</td>
</tr>
<tr>
  <td>リンク色</td>
  <td><input type=text name=vl size=12 value="$vl">
	<font color="$vl">■</font> （訪問済）</td>
</tr>
<tr>
  <td>リンク色</td>
  <td><input type=text name=al size=12 value="$al">
	<font color="$al">■</font> （訪問中）</td>
</tr>
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>記事題名色</td>
  <td><input type=text name=subcol size=12 value="$subcol">
	<font color="$subcol">■</font></td>
</tr>
<tr>
  <td>引用符色</td>
  <td><input type=text name=refcol size=12 value="$refcol">
	<font color="$refcol">■</font></td>
</tr>
<tr>
  <td>戻り先</td>
  <td><input type=text name=home size=40 value="$home"></td>
</tr>
<tr>
  <td>最大記事数</td>
  <td><input type=text name=max size=5 value="$max"></td>
</tr>
<tr>
  <td>表\示件数</td>
  <td><input type=text name=plog size=5 value="$plog">
	（1ページ当りの記事表\示数）</td>
</tr>
<tr>
  <td>本文文字</td>
  <td><input type=text name=b_size size=5 value="$b_size"> ピクセル</td>
</tr>
<tr>
  <td>URLリンク</td>
  <td>
EOM
	if ($link) {
		print "<input type=radio name=link value=1 checked>する\n",
		"<input type=radio name=link value=0>しない\n";
	} else {
		print "<input type=radio name=link value=1>する\n",
		"<input type=radio name=link value=0 checked>しない\n";
	}
	print "&nbsp;&nbsp;（記事中のURLを自動リンク）</td></tr>\n";
	print "<tr><td>投稿間隔</td><td>";
	print "<input type=text name=wait size=5 value=\"$wait\"> 秒 &nbsp; ";
	print "（同一ホストの連続投稿制御）</td></tr>\n";

	if ($sendmail) {
		print "<tr><td colspan=2><hr></td></tr>\n";
		print "<tr><td>Ｅメール</td>";
		print "<td><input type=text name=mail size=30 value=\"$mail\"><br>\n";
		print "（メール通知する場合）</td></tr>\n";
	}

	print <<"EOM";
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>拒否ホスト</td>
  <td><input type=text name=deny size=40 value="$deny"><br>
	（アクセス拒否するホスト情報をスペースで区切る）</td>
</tr>
<tr><td colspan=2><hr></td></tr>
</table>
<input type=submit value="上記設定を修正する"></form>
</body>
</html>
EOM
	exit;
}


__END__

