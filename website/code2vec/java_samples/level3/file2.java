void x (int N){
    int num1 = 0, num2=1;
    int count = 0;

    
    while(counter < N){
        
        System.out.print(num1 + " ");

        int num3 = num2 + num1;
        num1 = num2;
        num2 = num3;
        count = count +1;
    }
}