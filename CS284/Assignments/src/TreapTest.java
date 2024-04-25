//Student: Aidan Fischer
//Homework 3
//Pledge: I pledge my honor that I have abided by the Stevens Honor System

import org.junit.Test;
import static org.junit.Assert.*;
import Treap;
public class TreapTest {
	@Test
	public void testAddNoRandomAndToString() {
		Treap<Character> test = new Treap<Character>();
		Character p = "p".charAt(0);
		Character g = "g".charAt(0);
		Character u = "u".charAt(0);
		Character a = "a".charAt(0);
		Character j = "j".charAt(0);
		Character r = "r".charAt(0);
		Character z = "z".charAt(0);
		Character w = "w".charAt(0);
		Character v = "v".charAt(0);
		Character x = "x".charAt(0);
		Character[] chars = {p,g,u,a,j,r,z,w,v,x};
		int[] ps = {99,80,75,60,65,40,47,32,21,25};
		for(int i = 0;i<chars.length;i++) {
			test.add(chars[i],ps[i]);
		}
		assertEquals("(key=p, priority=99)\n"
				+ "  (key=g, priority=80)\n"
				+ "    (key=a, priority=60)\n"
				+ "      null\n"
				+ "      null\n"
				+ "    (key=j, priority=65)\n"
				+ "      null\n"
				+ "      null\n"
				+ "  (key=u, priority=75)\n"
				+ "    (key=r, priority=40)\n"
				+ "      null\n"
				+ "      null\n"
				+ "    (key=z, priority=47)\n"
				+ "      (key=w, priority=32)\n"
				+ "        (key=v, priority=21)\n"
				+ "          null\n"
				+ "          null\n"
				+ "        (key=x, priority=25)\n"
				+ "          null\n"
				+ "          null\n"
				+ "      null\n",test.toString());
	}
	@Test
	public void testAddRandomAndFind() {
		Treap<Character> test = new Treap<Character>();
		Character p = "p".charAt(0);
		Character g = "g".charAt(0);
		Character u = "u".charAt(0);
		Character a = "a".charAt(0);
		Character j = "j".charAt(0);
		Character r = "r".charAt(0);
		Character z = "z".charAt(0);
		Character w = "w".charAt(0);
		Character v = "v".charAt(0);
		Character x = "x".charAt(0);
		Character[] chars = {p,g,u,a,j,r,z,w,v,x};
		for(Character c:chars) {
			test.add(c);
		}
		for(Character c:chars) {
			assertTrue(c.toString()+" not found",test.find(c));
		}
	}
	@Test
	public void testDelete() {
		Treap<Character> test = new Treap<Character>();
		Character p = "p".charAt(0);
		Character g = "g".charAt(0);
		Character u = "u".charAt(0);
		Character a = "a".charAt(0);
		Character j = "j".charAt(0);
		Character r = "r".charAt(0);
		Character z = "z".charAt(0);
		Character w = "w".charAt(0);
		Character v = "v".charAt(0);
		Character x = "x".charAt(0);
		Character[] chars = {p,g,u,a,j,r,z,w,v,x};
		Character[] chars2 = {p,u,a,j,r,z,w,v,x};
		for(Character c:chars) {
			test.add(c);
		}
		assertTrue(g.toString()+" not found",test.find(g));
		assertTrue("g deletion failed",test.delete(g));
		assertFalse("G didn't get removed",test.find(g));
		for(Character c:chars2) {
			assertTrue(c.toString()+" not found",test.find(c));
		}
	}
}
