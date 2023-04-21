
static void x(int a[]){
    int l = a.length;

    for(int i=0; i< l - 1; i++){

        for(int j = 0; j < l - i - 1; j++){

            if(a[j] > a[j+1]){
                int temp = a[j];
                a[j]= a[j + 1];
                a[j + 1] = temp;
            }
        }
    }
}