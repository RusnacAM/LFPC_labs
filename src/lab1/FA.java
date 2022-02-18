package lab1;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class FA {
    static ArrayList<String> prodr = new ArrayList<>();
    static ArrayList<Character> vn = new ArrayList<>();
    static ArrayList<Character> col1 = new ArrayList<>();
    static ArrayList<Character> col2 = new ArrayList<>();
    static int prodSize = 0;
    static String word = "aabcab";


    public static void main(String[] args) {
        //Get text from file
        try {
            File myObj = new File("src/lab1/production.txt");
            Scanner reader = new Scanner(myObj);
            while (reader.hasNextLine()) {
                prodr.add(reader.nextLine());
                prodSize++;
            }
            reader.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }

        System.out.println(prodr);

        //Function to get only nonterminal symbols
        getNonterminal(prodr);

        //Initializez the Array
        int size = vn.size() + 1;
        Integer[][] finalMatrix = new Integer[size][size];

        for(int i = 0; i < finalMatrix.length; i++){
            Arrays.fill(finalMatrix[i], 0);
        }

        // Get indexes and form matrix
        getIndexes(finalMatrix);

        //Check if input string is accepted
        System.out.println("The word " + word + " is valid: " + wordCheck(word));

    }

    public static void getNonterminal(ArrayList<String> prodRules) {

        for (int i = 0; i < prodRules.size(); i++) {
            String str = prodRules.get(i);
            char ch = str.charAt(0);
            col1.add(ch);
        }

        for(int i = 0; i < prodRules.size(); i++){
            String str = prodRules.get(i);
            char ch = str.charAt(str.length() - 1);
            col2.add(ch);
        }

        for(int i = 0; i < col1.size(); i++){
            boolean flag = false;
            for(int j = 0; j < i; j++){
                if(col1.get(i) == col1.get(j)){
                    flag = true;
                    break;
                }
            } if(!flag){
                vn.add(col1.get(i));
            }
        }

        System.out.println(col1);
        //System.out.println(col2);
        System.out.println(vn);

    }

    public static void getIndexes(Integer[][] matrix) {

        ArrayList<Integer> colPos = new ArrayList<>();
        ArrayList<Integer> rowPos = new ArrayList<>();

        for(int i = 0; i < col1.size(); i++){
            for(int j = 0; j < vn.size(); j++){
                if(col1.get(i) == vn.get(j)){
                    rowPos.add(vn.indexOf(vn.get(j)));
                }
            }
        }

        for(int i = 0; i < col2.size(); i++){
            for(int j = 0; j < vn.size(); j++){
                if(col2.get(i) == vn.get(j)){
                    colPos.add(vn.indexOf(vn.get(j)));
                } else if (Character.isLowerCase(col2.get(i))){
                    colPos.add(vn.size());
                    break;
                }
            }
        }

        //System.out.println(rowPos);
        //System.out.println(colPos);

        for(int i = 0; i < prodSize; i++){
            matrix[rowPos.get(i)][colPos.get(i)] = 1;
        }

        System.out.println(Arrays.deepToString(matrix));

    }

    public static boolean wordCheck(String toCheck){

        String[] wordTemp = toCheck.split("");
        String nextVn = "S";
        int count = 0 ;

        for(int i = 0; i < wordTemp.length; i++){
            for(int j = 0; j < prodSize; j++){
                if(prodr.get(j).substring(0, 1).equals(nextVn) && prodr.get(j).substring(2, 3).equals(wordTemp[i])){
                    count++;
                    if(Character.isUpperCase(prodr.get(j).charAt(prodr.get(j).length() - 1)) && i != wordTemp.length - 1){
                        nextVn = Character.toString(prodr.get(j).charAt(prodr.get(j).length() - 1));
                        break;
                    } else {
                        nextVn = null;
                    }
                }
            }
        }
        if(count == wordTemp.length && nextVn == null) {
            return true;
        } else {
            return false;
        }
    }

}


