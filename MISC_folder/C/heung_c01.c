int mystFunc(int x, int y){
if(x<2){
x=y-x;
return x;
}else{
    int nX=x-2;
    int nY=y-x;
    int ret= mystFunc(nX, nY);
    printf("%d, %d, %d, %d\n", x, y, nX, nY);
    return ret + x;
    }
}
int result = mystFunc(5, 14);
printf("%d\n",result);