package lab2;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Scanner;

public class Lab2 {
    static LinkedHashMap<String, LinkedHashMap<String, List<String>>> NFA = new LinkedHashMap<>();
    static String startState = "q0";
    static String finalState = "q3";
    public static void main(String[] args) {

        try {
            File myObj = new File("src/lab2/NFA.txt");
            Scanner reader = new Scanner(myObj);
            while (reader.hasNextLine()) {
                String toSplit = reader.nextLine();
                String[] states = toSplit.split("[,=]");
                Data.buildTransition(NFA, states[0], states[1], states[2]);
            }
            reader.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }

        System.out.println("Initial NFA: ");
        for(String key: NFA.keySet()){
            System.out.println(key + " = " + NFA.get(key));
        }

        //System.out.println(" ");
        Conversion.buildDFA(NFA, startState, finalState);

    }

}
