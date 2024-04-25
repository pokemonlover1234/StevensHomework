//Name: Aidan Fischer
//Pledge: I pledge my honor that I have abided by the Stevens Honor System/
public class PairLinkedList {
	
	private static class Node {
		  private Integer data;
		  private Node next;
		  /** Creates a new node with a null next field
		      @param dataItem  The data stored
		  */
		  
		  private Node(int dataItem) {
		    data = dataItem;
		    next = null;
		  }	 
	}

	private static class Pair {
		  private Integer data;
		  private Integer copy_count;
		  private Pair next;
		  /** Creates a new pair with a null next field
		      @param dataItem  The data stored
		  */
		  
		  private Pair(Integer dataItem) {
		    data = dataItem;
		    next = null;
		  }	 
		  
		  /**
		   * set the number of copies as copy
		   * @param copy
		   */
		  private void set_copy(Integer copy) {
			  copy_count = copy;
		  }
	}
	
	Pair head;
	
	/**
	 * return the string of the linked list
	 */
	public String toString() {
	    StringBuilder sb = new StringBuilder("[");
	    Pair p = head;
	    if (p != null) {
	        while (p.next != null) {
	            sb.append(p.data.toString());
	            sb.append(",");
	            sb.append(p.copy_count);
	            sb.append(" ==> ");
	            p = p.next;
	        }
	        sb.append(p.data.toString());
	        sb.append(",");
            sb.append(p.copy_count);
	    }
	    sb.append("]");
	    return sb.toString();
	}
	public void compress(Node node_head) {
		if(node_head==null) {
			throw new IllegalArgumentException("Can't compress from a null node");
		}
		Pair tmpPair = null;
		Node currentNode = node_head;
		int currentCount = 0;
		Integer currentValue = null;
		while(currentNode.next != null) {
			if(currentNode.data.intValue() % 2 == 0) {
				currentNode = currentNode.next;
				continue;
			}else {
				if(currentValue==null) {
					currentValue = currentNode.data;
					currentNode = currentNode.next;
					++currentCount;
					continue;
				}
				else if(currentNode.data.equals(currentValue)) {
					++currentCount;
					currentNode = currentNode.next;
				}
				else {
					if(tmpPair==null){
						tmpPair = new Pair(currentValue);
						tmpPair.set_copy(currentCount);
						this.head = tmpPair;
					}else {
						Pair newPair = new Pair(currentValue);
						newPair.set_copy(currentCount);
						tmpPair.next = newPair;
						tmpPair = newPair;
					}
					currentCount = 0;
					currentValue = null;
					currentNode = currentNode.next;
				}
			}
		}
		if(currentNode.data.intValue() % 2 != 0) {
			if(currentValue==null) {
				currentValue = currentNode.data;
				++currentCount;
			}
			else if(currentNode.data.equals(currentValue)) {
				++currentCount;
			}
			else if(tmpPair==null){
				tmpPair = new Pair(currentValue);
				tmpPair.set_copy(currentCount);
				this.head = tmpPair;
				currentCount = 0;
				currentValue = null;
			}else {
				Pair newPair = new Pair(currentValue);
				newPair.set_copy(currentCount);
				tmpPair.next = newPair;
				tmpPair = newPair;
				currentCount = 0;
				currentValue = null;
			}

		}
		if(currentValue==null) {
			currentValue = currentNode.data;
			++currentCount;
		}
		else if(currentNode.data.equals(currentValue)) {
			++currentCount;
		}
		if(tmpPair==null){
			tmpPair = new Pair(currentValue);
			tmpPair.set_copy(currentCount);
			this.head = tmpPair;
		}else {
			Pair newPair = new Pair(currentValue);
			newPair.set_copy(currentCount);
			tmpPair.next = newPair;
		}
	}
	
	public static void main(String[] args) {
		
	    Node n1 = new Node(3);
	    Node n2 = new Node(3);
	    Node n3 = new Node(2);
	    Node n4 = new Node(3);
	    Node n5 = new Node(2);
	    Node n6 = new Node(1);
	    Node n7 = new Node(1);
	    Node n8 = new Node(3);
	    //Node n9 = new Node(2);
	    //Node n10 = new Node(1);
	    //Node n11 = new Node(1);
	    
	    n1.next = n2;
	    n2.next = n3;
	    n3.next = n4;
	    n4.next = n5;
	    n5.next = n6;
	    n6.next = n7;
	    n7.next = n8;
	    //n8.next = n9;
	    //n9.next = n10;
	    //n10.next = n11;
	    
	    PairLinkedList pll = new PairLinkedList();
	    pll.compress(n1);
	    
	    System.out.println(pll.toString());
	}
}
