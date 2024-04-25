import java.util.HashSet;
import java.util.Random;
import java.util.Stack;
//Student: Aidan Fischer
//Homework 3
//Pledge: I pledge my honor that I have abided by the Stevens Honor System
public class Treap<E extends Comparable<E>> {
	private static class Node<E>{
		E data;
		int priority;
		Node<E> left;
		Node<E> right;
		
		public Node(E data, int priority) {
			if(data == null) {
				throw new IllegalArgumentException("Data cannot be null");
			}
			this.data = data;
			this.priority = priority;
			left = null;
			right = null;
		}
		
		public Node<E> rotateRight() {
			Node<E> thisleft = this.left;
			Node<E> thisright = this.right;
			Node<E> thisleftleft = null;
			Node<E> thisleftright = null;
			if(thisleft==null) {
				return this;
			}else {
				thisleftleft = thisleft.left;
				thisleftright = thisleft.right;
			}
			Node<E> newRoot = new Node<E>(thisleft.data,thisleft.priority);
			newRoot.left=thisleftleft;
			newRoot.right=new Node<E>(this.data,this.priority);
			newRoot.right.left=thisleftright;
			newRoot.right.right=thisright;
			this.left = newRoot.left;
			this.right = newRoot.right;
			this.data = newRoot.data;
			this.priority = newRoot.priority;
			return newRoot;
		}
		public Node<E> rotateLeft() {
			Node<E> thisleft = this.left;
			Node<E> thisright = this.right;
			Node<E> thisrightleft = null;
			Node<E> thisrightright = null;
			if(thisright==null) {
				return this;
			}else {
				thisrightleft = thisright.left;
				thisrightright = thisright.right;
			}
			Node<E> newRoot = new Node<E>(thisright.data,thisright.priority);
			newRoot.left = new Node<E>(this.data,this.priority);
			newRoot.right = thisrightright;
			newRoot.left.left = thisleft;
			newRoot.left.right = thisrightleft;
			this.left = newRoot.left;
			this.right = newRoot.right;
			this.data = newRoot.data;
			this.priority = newRoot.priority;
			return newRoot;
		}
		public String toString() {
			return toString(0);
		}
		public String toString(int depth) {
			StringBuilder s = new StringBuilder();
			for(int i = 0; i<depth;i++) {
				s.append("  ");
			}
			s.append("(key=");
			s.append(data.toString());
			s.append(", priority=");
			s.append(priority);
			s.append(")\n");
			if(left==null) {
				for(int i = 0; i<=depth;i++) {
					s.append("  ");
				}
				s.append("null\n");
			}else {
				s.append(left.toString(depth+1));
			}
			if(right==null) {
				for(int i = 0; i<=depth;i++) {
					s.append("  ");
				}
				s.append("null\n");
			}else {
				s.append(right.toString(depth+1));
			}
			return s.toString();
		}
	}
	
	private Random priorityGenerator;
	private Node<E> root;
	private HashSet<Integer> priorities = new HashSet<Integer>();
	
	
	//Use a HashSet to maintain uniqueness of randomized heap priorities.
	private Integer getNewPriority() {
		Integer size = priorities.size();
		Integer newPriority = 0;
		while(priorities.size() == size) {
			newPriority = priorityGenerator.nextInt();
			priorities.add(newPriority);
		}
		//This seems counter-intuitive, but the purpose is so add(E key, int priority) can 
		//maintain uniqueness if someone wants to add their own priority for some reason,
		//without using random values.
		priorities.remove(newPriority);
		return newPriority;
	}
	
	public Treap() {
		priorityGenerator = new Random();
		root = null;
	}
	
	public Treap(long seed) {
		priorityGenerator = new Random(seed);
		root = null;
	}
	
	boolean add(E key) {
		return add(key, getNewPriority());
	}
	boolean add(E key, int priority) {
		//Maintain uniqueness by making sure the priority is unique.
		int size = priorities.size();
		priorities.add(priority);
		if(priorities.size() == size) {
			return false;
		}
		Node<E> newNode = new Node<E>(key, priority);
		//If the treap is empty, initialize it by setting root
		if(root == null) {
			root = newNode;
		}else {
			Node<E> curNode = root;
			Stack<Node<E>> path = new Stack<Node<E>>();
			path.add(root);
			while(curNode.left != null || curNode.right != null){
				if(newNode.data.compareTo(curNode.data) < 0) {
					if(curNode.left != null){
						curNode = curNode.left;
					}else {
						break;
					}
				}else if(newNode.data.compareTo(curNode.data) == 0) {
					return false;
				}else {
					if(curNode.right != null) {
						curNode = curNode.right;
					}else {
						break;
					}
				}
				path.add(curNode);
			}
			if(newNode.data.compareTo(curNode.data) < 0) {
				curNode.left = newNode;
				path.add(newNode);
			}else if(newNode.data.compareTo(curNode.data) == 0) {
				return false;
			}else {
				curNode.right = newNode;
				path.add(newNode);
			}
			reheap(path);
		}
		return true;
	}
	private void reheap(Stack<Node<E>> path) {
		if(path.size()<=1) {
			return;
		}
		Node<E> current = path.pop();
		Node<E> prev = path.peek();
		Integer p = current.priority;
		while(current.priority>prev.priority) {
			if(prev.left!=null && prev.right!=null) {
				if(prev.left.priority == p) {
					prev.rotateRight();
				}else if(prev.right.priority == p) {
					prev.rotateLeft();
				}
			}
			else if(prev.left!=null) {
				if(prev.left.priority == p) {
					prev.rotateRight();
				}
			}else if(prev.right!=null) {
				if(prev.right.priority == p) {
					prev.rotateLeft();
				}
			}
			if(path.size()<=1) {
				break;
			}
			current = prev;
			prev = path.pop();
			p=current.priority;
		}
	}
	boolean delete(E key) {
		Node<E> curNode = root;
		while(curNode.left != null || curNode.right != null){
			if(curNode.data.compareTo(key) > 0) {
				if(curNode.left != null){
					curNode = curNode.left;
				}else {
					break;
				}
			}else if(curNode.data.compareTo(key) == 0) {
				break;
			}else {
				if(curNode.right != null) {
					curNode = curNode.right;
				}else {
					break;
				}
			}
		}
		if(curNode.data.compareTo(key) == 0) {
			while(curNode.left != null || curNode.right != null) {
				if(curNode.left != null && curNode.right != null) {
					if(curNode.right.data.compareTo(curNode.left.data) < 0) {
						curNode.rotateRight();
						curNode = curNode.right;
					}else {
						curNode.rotateLeft();
						curNode = curNode.left;
					}
				}if(curNode.left==null) {
					curNode.rotateLeft();
					curNode = curNode.left;
				}else {
					curNode.rotateRight();
					curNode = curNode.right;
				}
			}
			System.out.println(root.data);
			curNode = root;
			Stack<Node<E>> path = new Stack<Node<E>>();
			path.add(root);
			while(curNode.left != null || curNode.right != null){
				if(curNode.data.compareTo(key) > 0) {
					if(curNode.left != null){
						curNode = curNode.left;
						path.add(curNode);
					}else {
						break;
					}
				}else if(curNode.data.compareTo(key) == 0) {
					break;
				}else {
					if(curNode.right != null) {
						curNode = curNode.right;
						path.add(curNode);
					}else {
						break;
					}
				}
			}
			Node<E> toDelete = path.pop();
			if(path.size()==0) {
				if(toDelete.data.compareTo(root.data) == 0) {
					root = null;
				}
				if(root.left!=null) {
					if(toDelete.data.compareTo(root.left.data) == 0) {
						root.left = null;
					}
				}
				if(root.right!=null) {
					if(toDelete.data.compareTo(root.right.data) == 0) {
						root.right = null;
					}
				}
			}
			else {
				if(path.peek().left!=null) {
					if(path.peek().left.data.compareTo(toDelete.data) == 0) {
						path.peek().left = null;
					}else {
						path.peek().right = null;
					}
				}else {
					path.peek().right = null;
				}
			}
			return true;
		}else {
			return false;
		}
	}
	boolean find(E key) {
		return find(root, key);
	}
	private boolean find(Node<E> root, E key) {
		Node<E> curNode = root;
		while(curNode.left != null || curNode.right != null){

			if(curNode.data.compareTo(key) > 0) {
				if(curNode.left != null){
					curNode = curNode.left;
				}else {
					break;
				}
			}else if(curNode.data.compareTo(key) == 0) {
				return true;
			}else {
				if(curNode.right != null) {
					curNode = curNode.right;
				}else {
					break;
				}
			}
		}
		if(curNode.data.compareTo(key) == 0) {
			return true;
		}
		return false;
	}
	public String toString() {
		return root.toString();
	}
	
	//Have to test Node in main class file cause Node is a private inner class.
	public static void TestNodeRotate() {
		Node<String> t = new Node<String>("t",8);
		Node<String> q = new Node<String>("q",9);
		Node<String> u = new Node<String>("u",7);
		Node<String> a = new Node<String>("a",2);
		Node<String> r = new Node<String>("r",0);
		t.left = q;
		t.right = u;
		q.left = a;
		q.right =  r;
		Node<String> root = t.rotateRight();
		if (root.data != "q") throw new IllegalStateException("Rotation right isn't working properly: root.data is " + root.data);
		if (root.left.data != "a") throw new IllegalStateException("Rotation right isn't working properly: root.left.data is " + root.left.data);
		if (root.right.data != "t") throw new IllegalStateException("Rotation right isn't working properly: root.right.data is " + root.right.data);
		if (root.right.left.data != "r") throw new IllegalStateException("Rotation right isn't working properly: root.right.left.data is " + root.right.left.data);
		if (root.right.right.data != "u") throw new IllegalStateException("Rotation right isn't working properly: root.right.right.data is " + root.right.right.data);
		
		root = root.rotateLeft();
		if (root.data != "t") throw new IllegalStateException("Rotation left isn't working properly: root.data is " + root.data);
		if (root.left.data != "q") throw new IllegalStateException("Rotation left isn't working properly: root.left.data is " + root.left.data);
		if (root.right.data != "u") throw new IllegalStateException("Rotation left isn't working properly: root.right.data is " + root.right.data);
		if (root.left.left.data != "a") throw new IllegalStateException("Rotation left isn't working properly: root.left.left.data is " + root.left.left.data);
		if (root.left.right.data != "r") throw new IllegalStateException("Rotation left isn't working properly: root.left.right.data is " + root.left.right.data);
		
	}
	
	public static void main(String[] args) {
		TestNodeRotate();
	}
}
