#include<iostream>

using namespace std;

int knapsack_01(int W, int Weight[], int Profit[], int n)
{
    //W is total capacity of knapsack
    //n is the number of items available to us

    //Base Case
    if(n == 0 || W == 0)
        return 0;

    //If the weight of the nth item is more than Knapsack capacity W, then
    //this item cannot be included in the optimal solution
    else if(Weight[n-1] > W)
        return knapsack_01(W, Weight, Profit, n-1);

    //Return the maximum of the two cases:
    //(1) nth item included
    //(2) not include
    else
        return max(Profit[n-1] + knapsack_01(W - Weight[n-1],Weight,Profit,n-1), knapsack_01(W, Weight, Profit, n-1));   
}

int knapsack(int W, int Weight[], int Profit[], int n)
{
    int i, w;
    int K[n+1][W+1];

    //Build table k[][] in bottom up manner
    for(i=0; i<=n; i++)
    {
        for(w=0; w<=W; w++)
        {
            if(i == 0 || w == 0)
                K[i][w] = 0;

            else if(Weight[i-1] > W)
                K[i][w] = K[i-1][w];

            else
                K[i][w] = max(Profit[i-1] + K[i-1][w -Weight[i-1]], K[i-1][w]);
        }
    }

    return K[n+1][W+1];
}

int main()
{
    int Profit[3] = {10, 12, 28};
    int Weight[3] = {1, 2, 4};

    int MaxProfit1 = knapsack_01(6,Weight,Profit,3);
    int MaxProfit2 = knapsack_01(6,Weight,Profit,3);

    cout<<"The maximum profit is:"<<MaxProfit1;
    cout<<"\nThe maximum profit is:"<<MaxProfit2;

    return 0;
}