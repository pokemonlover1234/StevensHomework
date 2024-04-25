//Aidan Fischer
//I pledge my honor that I have abided by the Stevens Honor System

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;


public class Anagrams {
	final Integer[] primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101};
	Map<Character,Integer> letterTable;
	Map<Long,ArrayList<String>> anagramTable;
	
	public Anagrams() {
		anagramTable = new HashMap<Long,ArrayList<String>>();
		letterTable = new HashMap<Character,Integer>();
		buildLetterTable();
		
	}
	private void buildLetterTable() {
		char[] alphabet = "abcdefghijklmnopqrstuvwxyz".toCharArray();
		for(int i = 0; i<alphabet.length;i++) {
			letterTable.put(alphabet[i], primes[i]);
		}
	}
	private Long myHashCode(String s) {
		Long res = (long) 1;
		for(char c:s.toCharArray()) {
			res *= letterTable.get(c);
		}
		return res;
	}
	private void addWord(String s) {
		Long hash = myHashCode(s);
		if(!anagramTable.containsKey(hash)) {
			ArrayList<String> newStringList = new ArrayList<String>();
			newStringList.add(s);
			anagramTable.put(hash, newStringList);
		} else {
			anagramTable.get(hash).add(s);
		}
	}
	private ArrayList<Map.Entry<Long, ArrayList<String>>> getMaxEntries(){
		//Tracks the number representing the largest number of anagrams.
		int maxEntriesValue = 0;
		//Holds what are currently seen to be the words with largest number of anagrams.
		ArrayList<Map.Entry<Long, ArrayList<String>>> maxEntries = new ArrayList<Map.Entry<Long, ArrayList<String>>>();
		Set<Map.Entry<Long, ArrayList<String>>> entries = anagramTable.entrySet();
		for(Map.Entry<Long, ArrayList<String>> item: entries) {
			if(item.getValue().size()>maxEntriesValue) {
				//Update maximum value and clear maxEntries if it turns out there is a word with a larger
				//number of anagrams. No need to recheck all previous entries because all previous entries
				//must have a smaller number of anagrams now. Add this one to the ArrayList.
				maxEntriesValue = item.getValue().size();
				maxEntries.clear();
				maxEntries.add(item);
			}else if(item.getValue().size()==maxEntriesValue){
				//Otherwise if it's the same number of anagrams add it.
				maxEntries.add(item);
			}
		}
		return maxEntries;
	}
	public void processFile(String s) throws IOException {
		FileInputStream fstream = new FileInputStream(s);
		BufferedReader br = new BufferedReader(new InputStreamReader(fstream));
		String strLine;
		while((strLine = br.readLine()) != null) {
			this.addWord(strLine);
		}
		br.close();
	}
	public static void main(String[] args) {
		test();
		Anagrams a = new Anagrams();
		
		final long startTime = System.nanoTime();
		try {
			a.processFile("words_alpha.txt");
		} catch (IOException e1) {
			e1.printStackTrace();
		}
		ArrayList<Map.Entry<Long, ArrayList<String>>> maxEntries = a.getMaxEntries();
		final long estimatedTime = System.nanoTime() - startTime;
		final double seconds = ((double) estimatedTime/1000000000);
		System.out.println("Time:" + seconds);
		System.out.println("List of max anagrams: ");
		for(Map.Entry<Long, ArrayList<String>> entry:maxEntries) {
			System.out.println("   Key: " + entry.getKey());
			System.out.println("   Anagrams: " + entry.getValue());
		}
		System.out.println("Length of list of max anagrams: " + maxEntries.get(0).getValue().size());
	}
	
	public static void test() {
		Anagrams test = new Anagrams();
		Long hash = (long) 1;
		for(Integer i: test.primes) {
			hash *= (long) i;
		}
		if(!test.myHashCode("abcdefghijklmnopqrstuvwxyz").equals(hash)) {
			throw new IllegalStateException("Unexpected hash in test: " + test.myHashCode("abcdefghijklmnopqrstuvwxyz") + " != " + hash);
		}
	}
	
}
