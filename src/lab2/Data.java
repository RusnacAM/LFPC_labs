package lab2;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;

public class Data {

        static void buildTransition (LinkedHashMap<String, LinkedHashMap<String, List<String>>> nfa, String k1, String k2, String v){
        if(nfa.get(k1) == null){
                List<String> vals = new ArrayList<>();
                LinkedHashMap<String, List<String>> innerKey = new LinkedHashMap<>();
                vals.add(v);
                innerKey.put(k2, vals);
                nfa.put(k1, innerKey);
        } else if (nfa.get(k1).containsKey(k2)){
                List<String> vals = nfa.get(k1).get(k2);
                LinkedHashMap<String, List<String>> innerKey = nfa.get(k1);
                vals.add(v);
                innerKey.put(k2, vals);
                nfa.put(k1, innerKey);
        } else {
               List<String> vals = new ArrayList<>();
               LinkedHashMap<String, List<String>> innerKey = nfa.get(k1);
               vals.add(v);
               innerKey.put(k2, vals);
               nfa.put(k1, innerKey);
        }



    }

}
