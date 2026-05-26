#include <stdio.h>

int main(){
    int i,j,k,l;
    printf("Welcome to calculator\n\n\n");
    printf("1. Add\n2. Subtract\n3. Multiply\n4. Divide");
    scanf("%d", &i);

    if (i == 1){
        printf("Enter first number:");
        scanf("%d", &j);
        printf("Enter second number:");
        scanf("%d", &k);
        l = j + k;
        printf("%d + %d = %d", j,k,l);
    }
    else if (i == 2){
        printf("Enter first number:");
        scanf("%d", &j);
        printf("Enter second number:");
        scanf("%d", &k);
        l = j - k;
        printf("%d - %d = %d", j,k,l);
    }
    else if (i == 3){
        printf("Enter first number:");
        scanf("%d", &j);
        printf("Enter second number:");
        scanf("%d", &k);
        l = j*k;
        printf("%d * %d = %d", j,k,l);
    }
    else if (i == 4){
        printf("Enter first number:");
        scanf("%d", &j);
        printf("Enter second number:");
        scanf("%d", &k);
        l = j/k;
        printf("%d / %d = %d", j,k,l);
    }
    else{
        printf("\nonly enter the following values 1, 2, 3, and 4. Program shutting down.");
    }
    
}