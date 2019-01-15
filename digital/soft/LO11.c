#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include <time.h>

int main(void){
	char c;
	int cursor[2]={2,2},n,m,i,j,k,sum;
	int table[7][7];
	int lv=100;
	char buffer[6],randname[10];
	unsigned long int rand1;
	FILE *file;
	char filename[256];

	while(1){
		/*盤面の初期化*/
		for (i=0;i<7;i++){
			for (j=0;j<7;j++){
				table[i][j]=-1;
			}
		}
		printf("LIGHTS OUT  <Ver1.1>\n\t\t\t(C)2006 Ikadzuchi-Squeak\nControl:\n  [W]\n[A] [D]\n  [X]\nLight: [.]\n\nReset Game: [@]\nQuit Game: [Shift+Q]\n\n");
		printf("Game Select : ");
		scanf("%s",filename);
		file=fopen(filename,"r");
		/*ファイルが存在しない場合盤をランダムに生成*/
		if (file==NULL){
			sscanf(filename,"%d",&lv);
			if(lv>100)
				lv=100;
			sscanf(filename,"%s",randname);
			rand1=0;
			for(i=0;i<10;i++){
				rand1=(unsigned long)(rand1+(i+1)*randname[i]);
			}
			srand(rand1+lv);
			for (k=0;k<lv;k++){
				n=rand()%5+1;
				m=rand()%5+1;
				table[n][m]=-table[n][m];
				table[n+1][m]=-table[n+1][m];
				table[n][m+1]=-table[n][m+1];
				table[n-1][m]=-table[n-1][m];
				table[n][m-1]=-table[n][m-1];
			}
		}
		/*ファイル読み込み*/
		else{
			for (i=0;i<5;i++){
				fscanf(file,"%s",buffer);
				for (j=0;j<5;j++){
					if (buffer[j]=='-')
						table[j+1][i+1]=-1;
					else
						table[j+1][i+1]=1;
				}
			}
		fclose(file);
		}	
	
		clrscr();	
		for (n=0;n<5;n++){
			printf(" ");
			if (cursor[0]==n){					
				for(m=0;m<5;m++){						
					if (cursor[1]==m){
						printf("\b<");
						if(table[m+1][n+1]==-1)
							printf("->");
						else
							printf("o>");
					}
					else if(table[m+1][n+1]==(-1))
						printf("- ");
					else
						printf("o ");
				}
				printf("\n");
			}
			else {
				for(i=0;i<5;i++){
					if(table[i+1][n+1]==(-1))
						printf("- ");
					else
						printf("o ");
				}
				printf("\n");
			}	
		}
		/*入力判定*/
		while(1){
			if (kbhit()){
				c = getch();
				if (c=='a'){	/*移動*/
					if (cursor[1]>=1)
	                    cursor[1]--;
				}
				else if(c=='d'){
					if (cursor[1]<=3)
						cursor[1]++;
				}
				else if (c=='w'){
					if (cursor[0]>=1)
						cursor[0]--;
				}
				else if (c=='x'){
					if (cursor[0]<=3)
						cursor[0]++;
				}
				else if (c=='.'){	/*ライト反転*/
					table[cursor[1]+1][cursor[0]+1]=-table[cursor[1]+1][cursor[0]+1];
					table[cursor[1]][cursor[0]+1]=-table[cursor[1]][cursor[0]+1];
					table[cursor[1]+1][cursor[0]]=-table[cursor[1]+1][cursor[0]];
					table[cursor[1]+2][cursor[0]+1]=-table[cursor[1]+2][cursor[0]+1];
					table[cursor[1]+1][cursor[0]+2]=-table[cursor[1]+1][cursor[0]+2];
				}
				/*クリア判定*/
				sum=0;
				for(i=1;i<6;i++){
					for(j=1;j<6;j++)
						sum=sum+table[i][j];
				}
				if(sum==-25){
					clrscr();
				printf(" - - - - -\n - - - - -\n - CLEAR!-\n - - - - -\n - - - - -\n");
				}
				/*画面描画*/
				else{
					clrscr();
					for (n=0;n<5;n++){
						printf(" ");
						if (cursor[0]==n){					
							for(m=0;m<5;m++){						
								if (cursor[1]==m){
									printf("\b<");
									if(table[m+1][n+1]==-1)
										printf("->");
									else
									printf("o>");
								}			
								else if(table[m+1][n+1]==(-1))
									printf("- ");
								else
									printf("o ");
							}
							printf("\n");
						}
						else {
							for(i=0;i<5;i++){
								if(table[i+1][n+1]==(-1))
									printf("- ");
								else
									printf("o ");
							}
							printf("\n");
						}
					}
				}
				/*リセット*/
				if (c=='@'){
					clrscr();
					break;
				}
				/*終了*/
				if (c=='Q')
					return 0;		
			}
		}
	}
}