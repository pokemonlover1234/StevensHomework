//Student: Aidan Fischer
//CS284 Homework 3
//I pledge my honor that I have abided by the Stevens Honor System.

import java.util.LinkedList;
import java.util.Queue;
import java.util.Stack;

public class IsoTriangle {
	
	protected class Pair<E>{
		E value1;
		E value2;
		
		protected Pair(E value1, E value2) {
			this.value1 = value1;
			this.value2 = value2;
		}
	}

	protected class Node<E> {
		
		E value;
		
		Node<E> l_child;
		Node<E> r_child;
		
		Integer depth;
		
		private Node(E value, Node<E> l_child, Node<E> r_child) {
			this.value = value;
			this.l_child = l_child;
			this.r_child = r_child;
		}
		
		private Node(E value, Node<E> l_child, Node<E> r_child, int depth) {
			this.value = value;
			this.l_child = l_child;
			this.r_child = r_child;
			this.depth = depth;
		}
		
		private void set_depth(int depth) {
			this.depth = depth;
		}
		
		private int get_depth() {
			return this.depth;
		}
		
		private void set_value(E new_value) {
			this.value = new_value;
		}
	}
	
	public Node<Integer> build_tree_int() {
		Node<Integer> three = new Node<Integer>(3, null, null, 3);
		Node<Integer> four = new Node<Integer>(4, null, null, 3);
		
		
		Node<Integer> five = new Node<Integer>(5, null, null, 3);
		Node<Integer> six = new Node<Integer>(6, null, null, 3);
		
		Node<Integer> seven = new Node<Integer>(7, three, four, 2);
		Node<Integer> two = new Node<Integer>(2, five, six, 2);
		
		Node<Integer> zero = new Node<Integer>(0, seven, two, 1);
		
		return zero;
	}
	
	public Node<Integer> build_tree_int2() {
		
		Node<Integer> eleven = new Node<Integer>(11, null, null, 4);	
		Node<Integer> ten = new Node<Integer>(10, eleven, null, 4);	
				
		Node<Integer> eight = new Node<Integer>(8, null, null, 4);
		
		Node<Integer> nine = new Node<Integer>(9, ten, null, 4);
		
		Node<Integer> seven = new Node<Integer>(7, eight, nine, 4);
		
		
		Node<Integer> three = new Node<Integer>(3, seven, null, 3);
		Node<Integer> four = new Node<Integer>(4, null, null, 3);
		
		
		Node<Integer> five = new Node<Integer>(5, null, null, 3);
		Node<Integer> six = new Node<Integer>(6, null, null, 3);
		
		Node<Integer> one = new Node<Integer>(1, three, four, 2);
		Node<Integer> two = new Node<Integer>(2, five, six, 2);
		
		Node<Integer> zero = new Node<Integer>(0, one, two, 1);
		
		return zero;
	}
	
	
	Integer total_iso_triangle = 0;
	
	public Pair<Integer> count_iso_triangle(Node<Integer> root) {
		
		// handling terminal cases
		if (root == null) {
			return new Pair(0, 0);
		}
		
		Integer l_depth, r_depth;
		l_depth = r_depth = -1;
		
		if (root.l_child != null) {
			//return left_path_len to parent
			// pass nothing to children
			Pair<Integer> this_pair = count_iso_triangle(root.l_child);
			
			l_depth = this_pair.value1 + 1;
		}
		// handling terminal cases
		else
			l_depth = 0; 
		
		if (root.r_child != null) {
			// return right_path_len to parent
			// pass nothing to children
			Pair<Integer> this_pair = count_iso_triangle(root.r_child);
			
			r_depth = this_pair.value2 + 1;
		}
		// handling terminal cases
		else
			r_depth = 0;
		
		// update optimal solution
		total_iso_triangle += Math.min(l_depth, r_depth);
		
		Pair<Integer> ret_pair = new Pair(l_depth, r_depth);
		return ret_pair;
		
	}
	
	
	/**
	 * 4-step process
	 * (1) Pass parent's upper path len and direction to child
	 * A direction of -1 is left, 1 is right
	 * (2) Return left and right path len to parent
	 * (3) Terminal cases are where the left/right path we
	 * are checking ends, return (l/r)_depth = 0
	 * (4) Update solution based on formula.
	 * for type 2 and type 3 iso triangles, the formula is 
	 * min((l/r_depth),upper_path_len)
	 */
	
	public void count_iso_triangle2(Node<Integer> root){
		Pair<Integer> upper_l = new Pair<Integer>(0,-1);
		Pair<Integer> upper_r = new Pair<Integer>(0,1);
		//Start from root to both sides;
		count_iso_triangle2(root, upper_l);
		count_iso_triangle2(root, upper_r);
	}

	public Pair<Integer> count_iso_triangle2(Node<Integer> root, Pair<Integer> upper_path) {
		if (root == null) {
			return new Pair(0,0);
		}
		
		
		
		Integer l_depth,r_depth;
		l_depth = r_depth = -1;
		//Normalize directional input to -1 or 1, in case an erroneous direction is passed.
		Integer upper_len = upper_path.value1/(Math.abs(upper_path.value1));
		Integer upper_dir = upper_path.value2;
		
		if(upper_dir == -1) {
			if(root.l_child != null) {
				Pair<Integer> upper = new Pair<Integer>(upper_len + 1, -1);
				Pair<Integer> this_pair = count_iso_triangle2(root.l_child,upper);
				l_depth = this_pair.value1+1;
			}
			else {
				l_depth = 0;
			}
			if(root.r_child != null) {
				Pair<Integer> upper = new Pair<Integer>(0, -1);
				Pair<Integer> this_pair = count_iso_triangle2(root.r_child,upper);
				r_depth = this_pair.value2+1;
			}else {
				r_depth = 0;
			}
			total_iso_triangle += Math.min(upper_len, l_depth);
		}
		if(upper_dir == 1) {
			if(root.l_child != null) {
				Pair<Integer> upper = new Pair<Integer>(0, 1);
				Pair<Integer> this_pair = count_iso_triangle2(root.l_child,upper);
				l_depth = this_pair.value1+1;
			}
			else {
				l_depth = 0;
			}
			if(root.r_child != null) {
				Pair<Integer> upper = new Pair<Integer>(upper_len+1, 1);
				Pair<Integer> this_pair = count_iso_triangle2(root.r_child,upper);
				r_depth = this_pair.value2+1;
			}else {
				r_depth = 0;
			}
			total_iso_triangle += Math.min(upper_len, r_depth);
		}
		Pair<Integer> ret_pair = new Pair<Integer>(l_depth, r_depth);
		return ret_pair;
	}
	
	Integer max_iso_triangle = 0;
	
	public Pair<Stack<Integer>> max_iso_triangle(Node<Integer> root){
		max_iso_triangle = 0;
		Pair<Stack<Integer>> res = max_iso_triangle_helper(root);
		System.out.println(max_iso_triangle);
		return res;
	}
	
	public Pair<Stack<Integer>> max_iso_triangle_helper(Node<Integer> root) {
		Pair<Stack<Integer>> paths = new Pair(new Stack<Integer>(), new Stack<Integer>());
		// handling terminal cases
		if (root == null) {
			return paths;
		}
		
		if (root.l_child != null) {
			//Return the left path to parent
			//pass nothing to children
			paths.value1.add(root.l_child.value);
			paths.value1.addAll(max_iso_triangle_helper(root.l_child).value1);
		}
			
		
		if (root.r_child != null) {
			//Return right path to parent
			//pass nothing to children
			paths.value2.add(root.r_child.value);
			paths.value2.addAll(max_iso_triangle_helper(root.r_child).value2);

		}

		// update maximum solution
		if(paths.value1.size()>0 && paths.value2.size()>0)
			max_iso_triangle = Math.max(max_iso_triangle,root.value + paths.value1.peek() + paths.value2.peek());
		return paths;
	}
	
	
	public void test_count_iso_triangle() {
		IsoTriangle test = new IsoTriangle();
		Node<Integer> root = test.build_tree_int2();
		
		Pair<Integer> node = test.count_iso_triangle(root);
	}
	public void test_max_iso_triangle() {
		IsoTriangle test = new IsoTriangle();
		Node<Integer> root = test.build_tree_int2();
		//first test case
		root = test.build_tree_int2();
		Pair<Stack<Integer>> a = test.max_iso_triangle(root);
		//second test case
		root = test.build_tree_int();
		Pair<Stack<Integer>> b = test.max_iso_triangle(root);
	}
	public void test_count_iso_triangle2() {
		IsoTriangle test = new IsoTriangle();
		Node<Integer> root = test.build_tree_int();
		test.count_iso_triangle2(root);
		System.out.println("Total number of Type-2 and Type-3 iso triangles are:" + test.total_iso_triangle);
		test.total_iso_triangle=0;
		root = test.build_tree_int2();
		test.count_iso_triangle2(root);
		System.out.println("Total number of Type-2 and Type-3 iso triangles are:" + test.total_iso_triangle);
	}
	public static void main(String[] args) {
		
		IsoTriangle test = new IsoTriangle();
		test.test_count_iso_triangle2();
		
	}
}

