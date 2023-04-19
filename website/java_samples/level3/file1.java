// this method searcher an array for element
int x (int array[], int element, int low, int high){

    
    //repeat until the pointers low and high meet
    while (low <= high){

        //get index of mid element
        int mid=low + (high-low)/2

        // if elment search is the mid element
        if (array[mid] == element){
            return mid;
        }

        //if element is less than mid element
        //search only left side of min
        if(array[mid] < element){
            low = mid+1;
        }

        //if element is greater than mid element
        //search only right side of mid
        else{
            high = mid-1;
        }
    }

    return -1
}