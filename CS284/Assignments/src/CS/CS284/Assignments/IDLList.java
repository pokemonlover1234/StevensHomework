package CS.CS284.Assignments;
import java.util.ArrayList;


public class IDLList<E> {
	private class Node<E> {
		private E data;
		private Node<E> next;
		private Node<E> prev;
		
		Node (E elem){
			this.data = elem;
			this.next = null;
			this.prev = null;
		}
		Node (E elem, Node<E> prev, Node<E> next){
			this.data = elem;
			this.next = next;
			this.prev = prev;
		}
	}
	
	private Node<E> head;
	private Node<E> tail;
	private int size;
	//This is an indexed linked list
	private ArrayList<Node<E>> indices;
	
	public IDLList () {
		this.head = null;
		this.tail = null;
		this.size = 0;
		this.indices = new ArrayList<Node<E>>();
	}
	public boolean add(int index, E elem) {
		if(index > this.size) {
			throw new IllegalArgumentException("Index of inserted element must not be past end of list by more than one.");
		}else if(index < 0) {
			throw new IllegalArgumentException("Index of inserted element must be nonnegative");
		//The behavior when index is 0 and when index is this.size is the same as the 
		//other variations defined (add (no index) and append). Therefore, just call
		//those other functions here. Otherwise, we'd have code duplication.
		}else if(index == 0) {
			this.add(elem);
		}else if(index == this.size) {
			this.append(elem);
		}else {
			Node<E> newNode = new Node<E>(elem,this.indices.get(index-1),this.indices.get(index));
			this.indices.get(index-1).next = newNode;
			this.indices.get(index).prev = newNode;
			this.indices.add(index, newNode);
			++size;
		}
		return true;
	}
	public boolean add(E elem) {
		if(this.head != null) {
			Node<E> newNode = new Node<E>(elem,null,this.head);
			this.head.prev = newNode;
			this.head = newNode;
			this.indices.add(0, newNode);
		}else {
			Node<E> newNode = new Node<E>(elem);
			this.head = newNode;
			this.tail = newNode;
			this.indices.add(0, newNode);
		}
		++this.size;
		return true;
	}
	public boolean append(E elem) {
		if(this.tail == null) {
			Node<E> newNode = new Node<E>(elem);
			this.head = newNode;
			this.tail = newNode;
			this.indices.add(newNode);
		}else {
			Node<E> newNode = new Node<E>(elem,this.tail,null);
			this.tail.next = newNode;
			this.tail = newNode;
			this.indices.add(newNode);
		}
		++size;
		return true;
	}
	public E get(int index) {
		if(this.size == 0) {
			throw new IllegalStateException("Nothing to get from an empty list");
		}else if(index < 0) {
			throw new IllegalArgumentException("Index to get must be nonnegative");
		}else if(index > this.size - 1) {
			throw new IllegalArgumentException("Index to get must not exceed list length - 1");
		}
		return indices.get(index).data;
	}
	public E getHead() {
		if(this.head == null) {
			return null;
		}
		return this.head.data;
	}
	public E getLast() {
		if(this.tail == null) {
			return null;
		}
		return this.tail.data;
	}
	public int size() {
		return this.size;
	}
	public E remove() {
		if(this.head==null) {
			throw new IllegalStateException("List is empty, cannot remove from empty list.");
		}
		//If the removal operation would result in the set going empty, we must
		//treat this as a separate case. Otherwise we'd get index out of bounds
		//exceptions.
		else if(this.size == 1) {
			Node<E> tmp = this.head;
			this.indices.remove(0);
			this.head = null;
			this.tail = null;
			--this.size;
			return tmp.data;
		}
		Node<E> tmp = this.head;
		this.indices.get(1).prev = null;
		this.head = this.indices.get(1);
		this.indices.remove(0);
		--this.size;
		return tmp.data;
	}
	public E removeLast() {
		if(this.tail==null) {
			throw new IllegalStateException("List is empty, cannot remove from empty list.");
		}
		//Same situation here as in remove
		if(this.size == 1) {
			Node<E> tmp = this.tail;
			this.indices.remove(0);
			this.tail = null;
			this.head = null;
			--this.size;
			return tmp.data;
		}
		Node<E> tmp = this.tail;
		this.indices.get(this.size-2).next = null;
		this.tail = this.indices.get(this.size-2);
		this.indices.remove(this.size-1);
		--this.size;
		return tmp.data;
	}
	public E removeAt(int index) {
		if(this.size == 0) {
			throw new IllegalStateException("List is empty, cannot remove from empty list.");
		}else if(index < 0) {
			throw new IllegalArgumentException("Index to remove at must be nonnegative");
		}else if(index > this.size - 1){
			throw new IllegalArgumentException("Index to remove at must not exceed list length - 1");
		//Same situation here as in add (index)
		}else if(index == 0) {
			return this.remove();
		}else if(index == this.size - 1) {
			return this.removeLast();
		}else {
			Node<E> tmp = this.indices.get(index);
			this.indices.get(index-1).next = this.indices.get(index+1);
			this.indices.get(index+1).prev = this.indices.get(index-1);
			this.indices.remove(index);
			--this.size;
			return tmp.data;
		}
	}
	public boolean remove(E elem) {
		int index = 0;
		Node<E> current = this.head;
		if(current != null) {
			while(current.next != null) {
				if(current.data.equals(elem)) {
					//Don't duplicate code, just call the function already defined
					this.removeAt(index);
					return true;
				}
				++index;
				current = current.next;
			}
			return false;
		}
		else {
			return false;
		}
	}
	public String toString() {
		Node<E> current = this.head;
		StringBuilder sb = new StringBuilder("[");
		if(current != null) {
			while(current.next != null) {
				sb.append(current.data.toString());
				sb.append(" <=> ");
				current = current.next;
			}
			sb.append(current.data.toString());
		}
		sb.append("]");
		return sb.toString();
	}
}
