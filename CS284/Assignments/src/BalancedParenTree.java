import java.util.ArrayList;

public class BalancedParenTree {
	//Tree Node (represents a member of the parsed tree)
	private class Node {
		String terminal;
		Node[] children;
		
		Node(String terminal){
			this.terminal = terminal;
			this.children = null;
		}
		
		public void addChild(Node child) {
			if(this.children == null){
				this.children = new Node[1];
				this.children[0] = child;
				return;
			}
			Node[] newChildren = new Node[this.children.length + 1];
			for(int i = 0; i < this.children.length; i++) {
				newChildren[i] = this.children[i];
			}
			newChildren[this.children.length] = child;
			this.children = newChildren;
		}
	}
	
	public BalancedParenTree(String paren_str) {
		this.parse(paren_str);
	}
	
	public Node root;
	public void parse(String paren_str) {
		try {
			//Define tracking variables (may get very deep so keep track of previous nodes in an arraylist)
			Node root_node = new Node(null);
			Node current_node = root_node;
			ArrayList<Node> prev_nodes = new ArrayList<Node>();
			for(int i = 0; i < paren_str.length(); i++) {
				if(paren_str.substring(i, i + 1).equals("(")) {
					//Create the new node and traverse down a level to continue
					Node left_paren = new Node("(");
					Node new_child = new Node(null);
					new_child.addChild(left_paren);
					current_node.addChild(new_child);
					prev_nodes.add(0, current_node);
					current_node = new_child;
				}
				if(paren_str.substring(i, i + 1).equals(")")) {
					//Finish up the current node and traverse back up a level
					Node no_symbol = new Node("N");
					Node right_paren = new Node(")");
					if(current_node.children.length == 1) {
						current_node.addChild(no_symbol);
					}
					current_node.addChild(right_paren);
					current_node = prev_nodes.remove(0);
				}
			}
			if(!current_node.equals(root_node)) {
				throw new IllegalArgumentException("Imbalanced parenthesis passed to parse function");
			}
			this.root = root_node;
		}
		catch(IndexOutOfBoundsException e){
			throw new IllegalArgumentException("Imbalanced parenthesis passed to parse function");
		}
	}
	
	public void print() {
		print_recursive(this.root);
		System.out.println("");
	}
	
	public void print_recursive(Node current) {
		//Recursively traverse the tree to print back out the original string.
		if(current.children != null) {
			for(int i = 0; i < current.children.length; i++) {
				print_recursive(current.children[i]);
			}
		} else {
			if(current.terminal.equals("N")) {
				return;
			}
			System.out.print(current.terminal);
		}
	}
}
