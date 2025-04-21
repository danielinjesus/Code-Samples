#include <stdio.h> // Include standard input/output library for printf function

// Define a recursive function named mystFunc that takes two integers, x and y.
int mystFunc(int x, int y) {
    // Base case for the recursion: if x is less than 2
    if (x < 2) {
        x = y - x; // Perform a calculation using the current y and x
        return x;  // Return the result, stopping the recursion for this branch
    }
    // Recursive step: if x is 2 or greater
    else {
        // Calculate a new value for 'x' to be passed in the recursive call
        int nX = x - 2;
        // Calculate a new value for 'y' to be passed in the recursive call
        int nY = y - x;

        // Call the function itself (recursion) with the newly calculated values nX and nY
        int ret = mystFunc(nX, nY);

        // This print statement executes *after* the recursive call above has returned.
        // It shows the values of x, y, nX, and nY at this level of the recursion stack.
        printf("Returning from call where x=%d, y=%d: (nX=%d, nY=%d, returned value from deeper call=%d)\n", x, y, nX, nY, ret);

        // Return the value received from the deeper recursive call ('ret') added to the current value of 'x'
        return ret + x;
    }
}

// --- Execution starts here (assuming this is part of a main function or called elsewhere) ---

// Call the mystFunc function with initial values x=5 and y=14. Store the final result.
int result = mystFunc(5, 14);

// Print the final computed result to the console.
printf("Final result: %d\n", result);

/*
Note: To make this code runnable, you would typically wrap the last two lines
      within a main function like this:

int main() {
    int result = mystFunc(5, 14);
    printf("Final result: %d\n", result);
    return 0; // Indicate successful execution
}

*/