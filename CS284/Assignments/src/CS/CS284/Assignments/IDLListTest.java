package CS.CS284.Assignments;
import org.junit.Test;
import org.junit.Before;
import org.junit.Rule;
import org.junit.rules.ExpectedException;
import static org.junit.Assert.*;
import IDLList;

public class IDLListTest {
	private IDLList<Integer> intCase;
	private IDLList<String> stringCase;
	private IDLList<String[]> arrayCase;
	
	@Before public void setup() {
		intCase = new IDLList<Integer>();
		stringCase = new IDLList<String>();
		arrayCase = new IDLList<String[]>();
	}
	
	
	@Test
	public void testInitialSize() {
		assertEquals("Integer case not 0 size on declaration",0,intCase.size());
		assertEquals("String case not 0 size on declaration",0,stringCase.size());
		assertEquals("Array case not 0 size on declaration",0,arrayCase.size());
	}
	@Test
	public void testInitialHead() {
		assertEquals("Integer case head not null on declaration",null,intCase.getHead());
		assertEquals("String case head not null on declaration",null,stringCase.getHead());
		assertArrayEquals("Array case head not null on declaration",null,arrayCase.getHead());
	}
	@Test
	public void testInitialTail() {
		assertEquals("Integer case tail not null on declaration",null,intCase.getLast());
		assertEquals("String case tail not null on declaration",null,stringCase.getLast());
		assertArrayEquals("Array case tail not null on declaration",null,arrayCase.getLast());
	}
	@Test
	public void testAddNoIndex() {
		for(int i = 9; i >= 0; --i) {
			intCase.add(i);
			stringCase.add(i+"");
			String[] array = {i+""};
			arrayCase.add(array);
		}
		String[] test = {"0"};
		String[] test2 = {"9"};
		assertEquals("Head on int case should be 0",0,intCase.getHead().intValue());
		assertEquals("Head on string case should be \"0\"","0",stringCase.getHead());
		assertArrayEquals("Head on array case should be {0}",test,arrayCase.getHead());
		assertEquals("Tail on int case should be 9",9,intCase.getLast().intValue());
		assertEquals("Tail on string case should be \"9\"","9",stringCase.getLast());
		assertArrayEquals("Tail on array case should be {9}",test2,arrayCase.getLast());
		assertEquals("toString on int case should be same as string case",stringCase.toString(),intCase.toString());
	}
	@Test
	public void testAddIndexAndGetIndexInt() {
		intCase.add(0,0);
		intCase.add(1,1);
		intCase.add(2,2);
		intCase.add(1,3);
		assertEquals("Integer at index 0 should be 0",0,intCase.get(0).intValue());
		assertEquals("Integer at index 1 should be 3",3,intCase.get(1).intValue());
		assertEquals("Integer at index 2 should be 1",1,intCase.get(2).intValue());
		assertEquals("Integer at index 3 should be 2",2,intCase.get(3).intValue());
	}
	@Test
	public void testAddIndexAndGetIndexString() {
		stringCase.add(0,"0");
		stringCase.add(1,"1");
		stringCase.add(2,"2");
		stringCase.add(1,"3");
		assertEquals("String at index 0 should be \"0\"","0",stringCase.get(0));
		assertEquals("String at index 1 should be \"3\"","3",stringCase.get(1));
		assertEquals("String at index 2 should be \"1\"","1",stringCase.get(2));
		assertEquals("String at index 3 should be \"2\"","2",stringCase.get(3));
	}
	@Test
	public void testAddIndexAndGetIndexArray() {
		String[] add1 = {"0"};
		String[] add2 = {"1"};
		String[] add3 = {"2"};
		String[] add4 = {"3"};
		arrayCase.add(0,add1);
		arrayCase.add(1,add2);
		arrayCase.add(2,add3);
		arrayCase.add(1,add4);
		assertArrayEquals("Array at index 0 should be {0}",add1,arrayCase.get(0));
		assertArrayEquals("Array at index 1 should be {3}",add4,arrayCase.get(1));
		assertArrayEquals("Array at index 2 should be {1}",add2,arrayCase.get(2));
		assertArrayEquals("Array at index 3 should be {2}",add3,arrayCase.get(3));
	}
	//This technically tests get too.
	@Test 
	public void testAppend() {
		intCase.append(1);
		intCase.append(2);
		intCase.append(3);
		stringCase.append("1");
		stringCase.append("2");
		stringCase.append("3");
		String[] add1 = {"1"};
		String[] add2 = {"2"};
		String[] add3 = {"3"};
		arrayCase.append(add1);
		arrayCase.append(add2);
		arrayCase.append(add3);
		assertEquals("Integer at index 0 should be 1",1,intCase.get(0).intValue());
		assertEquals("Integer at index 1 should be 2",2,intCase.get(1).intValue());
		assertEquals("Integer at index 2 should be 3",3,intCase.get(2).intValue());
		assertEquals("String at index 0 should be \"1\"","1",stringCase.get(0));
		assertEquals("String at index 1 should be \"2\"","2",stringCase.get(1));
		assertEquals("String at index 2 should be \"3\"","3",stringCase.get(2));
		assertArrayEquals("Array at index 0 should be {1}",add1,arrayCase.get(0));
		assertArrayEquals("Array at index 1 should be {2}",add2,arrayCase.get(1));
		assertArrayEquals("Array at index 2 should be {3}",add3,arrayCase.get(2));
	}
	@Test
	public void testGetters() {
		intCase.append(1);
		intCase.append(2);
		intCase.append(3);
		stringCase.append("1");
		stringCase.append("2");
		stringCase.append("3");
		String[] add1 = {"1"};
		String[] add2 = {"2"};
		String[] add3 = {"3"};
		arrayCase.append(add1);
		arrayCase.append(add2);
		arrayCase.append(add3);
		assertEquals("Head should be 1",1,intCase.getHead().intValue());
		assertEquals("Head should be \"1\"","1",stringCase.getHead());
		assertArrayEquals("Head should be {1}",add1,arrayCase.getHead());
		assertEquals("Tail should be 3",3,intCase.getLast().intValue());
		assertEquals("Tail should be \"3\"","3",stringCase.getLast());
		assertArrayEquals("Tail should be {3}",add3,arrayCase.getLast());
		assertEquals("Size should be 3",3,intCase.size());
		assertEquals("Size should be 3",3,stringCase.size());
		assertEquals("Size should be 3",3,arrayCase.size());
	}
	@Test(expected = IllegalArgumentException.class)
	public void assertAddPastEndOfListFails() {
		intCase.add(2,4);
	}
	@Test(expected = IllegalArgumentException.class)
	public void assertAddNegativeIndexFails() {
		intCase.add(-1,4);
	}
	@Test(expected = IllegalStateException.class)
	public void assertGetEmptyListFails() {
		intCase.get(4);
	}
	@Test(expected = IllegalArgumentException.class)
	public void assertGetPastEndOfListFails() {
		intCase.add(1);
		intCase.get(4);
	}
	@Test(expected = IllegalArgumentException.class)
	public void assertGetNegativeIndexFails() {
		intCase.add(1);
		intCase.get(-1);
	}
	@Test(expected = IllegalStateException.class)
	public void assertRemoveFromEmptyListFails() {
		intCase.remove();
	}
	@Test
	public void testRemove() {
		intCase.append(1);
		intCase.append(2);
		intCase.append(3);
		assertEquals("Returned from remove should be 1",1,intCase.remove().intValue());
		assertEquals("Head should be 2",2,intCase.getHead().intValue());
		assertEquals("Returned from remove should be 2",2,intCase.remove().intValue());
		assertEquals("Head should be 3",3,intCase.getHead().intValue());
		assertEquals("Returned from remove should be 3",3,intCase.remove().intValue());
		assertEquals("Head should be null",null,intCase.getHead());
		assertEquals("Tail should be null",null,intCase.getLast());
	}
	@Test(expected = IllegalStateException.class)
	public void assertRemoveAtFromEmptyListFails() {
		intCase.removeAt(3);
	}
	@Test(expected = IllegalArgumentException.class)
	public void assertRemoveAtPastEndOfListFails() {
		intCase.append(1);
		intCase.removeAt(3);
	}
	@Test(expected = IllegalArgumentException.class)
	public void assertRemoveAtNegativeIndexFails() {
		intCase.append(1);
		intCase.removeAt(-1);
	}
	@Test
	public void testRemoveAt() {
		intCase.append(1);
		intCase.append(2);
		intCase.append(3);
		intCase.append(4);
		assertEquals("Returned from remove should be 3",3,intCase.removeAt(2).intValue());
		assertEquals("Index 2 should be 4",4,intCase.get(2).intValue());
		assertEquals("Returned from remove should be 2",2,intCase.removeAt(1).intValue());
		assertEquals("Index 1 should be 4",4,intCase.get(1).intValue());
	}
	@Test(expected = IllegalStateException.class)
	public void assertRemoveLastEmptyListFails() {
		intCase.removeLast();
	}
	@Test
	public void testRemoveLast() {
		intCase.append(1);
		intCase.append(2);
		intCase.append(3);
		assertEquals("Returned from remove should be 3",3,intCase.removeLast().intValue());
		assertEquals("Tail should be 2",2,intCase.getLast().intValue());
		assertEquals("Returned from remove should be 2",2,intCase.removeLast().intValue());
		assertEquals("Tail should be 1",1,intCase.getLast().intValue());
		assertEquals("Returned from remove should be 1",1,intCase.removeLast().intValue());
		assertEquals("Head should be null",null,intCase.getHead());
		assertEquals("Tail should be null",null,intCase.getLast());
	}
	@Test
	public void testToString(){
		intCase.append(1);
		intCase.append(3);
		intCase.append(2);
		stringCase.append("1");
		stringCase.append("3");
		stringCase.append("2");
		assertEquals("[1 <=> 3 <=> 2]",intCase.toString());
		assertEquals(intCase.toString(),stringCase.toString());
	}

}

