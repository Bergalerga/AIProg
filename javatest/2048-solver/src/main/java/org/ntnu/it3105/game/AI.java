package org.ntnu.it3105.game;

import java.lang.reflect.Array;
import java.util.*;

/**
 * Created by berg on 13/10/15.
 */
public class AI {

    int depth;
    float alpha;

    public AI(int depth) {
        this.depth = depth;
        this.alpha = 0;
    }
    //Calls expectimax on the moves that are possible to do from this board state.
    //Returns a direction to move.
    public Direction getNextMove(Board board) {
        int[][] current = board.getBoard();
        float best = 0;
        Direction direction = null;
        for (Direction dir : Direction.values()) {
            int[][] move = Board.checkMove(current, dir);
            //Performs expectimax with all moves.
            if (!Arrays.deepEquals(current, move)) {
                float neighbour = expectimax(move, this.depth, false);
                if (neighbour > best) {
                    best = neighbour;
                    direction = dir;
                }
            }
        }
        return direction;
    }
    //Main algorithm.
    private float expectimax(int[][] board, int depth, boolean maximizing_player) {
        if (depth == 0) {
            float h = heuristic(board);
            return h;
        }
        //Max node
        if (maximizing_player) {
            this.alpha = Integer.MIN_VALUE;
            for (int[][] neighbour : getNeighbours(board)) {
                alpha = Math.max(alpha, expectimax(neighbour, depth - 1, false));
            }
        }
        //Change node
        else {
            //Return weighted average of all child nodes' values
            this.alpha = 0;
            int numberOfZeroes = Board.countZeroes(board);
            for (int x = 0; x < 4; x++) {
                for (int y = 0; y < 4; y++) {
                    if (board[x][y] == 0) {
                        numberOfZeroes += 1;
                        int[][] copy = Board.getCopy(board);
                        copy[x][y] = 2;
                        alpha += ((0.9 / numberOfZeroes) * expectimax(copy, depth - 1, true));
                        copy = Board.getCopy(board);
                        copy[x][y] = 4;
                        alpha += ((0.1) / numberOfZeroes) * expectimax(copy, depth - 1, true);
                    }
                }
            }
        }
        return this.alpha;
    }

    //Heuristic function
    public float heuristic(int[][] board) {

        double[][] gradient = {
                { 10, 9, 8, 7 },
                { 9, 5, 4, 3 },
                { 8, 4, 2, 2 },
                { 7, 3, 2, 1 }
        };
        double[][] snake = {
                { 16, 15, 14, 13 },
                { 12, 11, 10, 9 },
                { 8, 7, 6, 5 },
                { 4, 3, 2, 1 }
        };
        int zeroes = 0;
        int gradients = 0;
        int adjacent = 0;
        int totalsum = 0;


        for (int x = 0; x < 4; x++) {
            for (int y = 0; y < 4; y++) {
                if (board[x][y] == 0) {
                    zeroes += 1;
                }
                gradients += board[x][y]*gradient[x][y];
                totalsum += board[x][y];
                for (Map.Entry<Direction, Integer> entry :  getValuesOfAdjacentNodes(board, x, y).entrySet()){
                    if (board[x][y] == entry.getValue()){
                        adjacent += 1;
                    }
                }


            }
        }

        int average_sum_per_tile = totalsum / (16-zeroes);

        int weight = gradients/40;
        int h = zeroes*weight + adjacent*weight + gradients + average_sum_per_tile*weight;

        System.out.println("null: " + zeroes*weight);
        System.out.println("adjacent: " + adjacent*weight);
        System.out.println("gradient: " + gradients);
        System.out.println("average: " + average_sum_per_tile*weight);
        return h;
    }
    //Returns the boards for all 4 move directions.
    public ArrayList<int[][]> getNeighbours(int[][] board) {
        ArrayList<int[][]> neighbours = new ArrayList();
        for (Direction dir : Direction.values()) {
            neighbours.add(Board.checkMove(board, dir));
        }
        return neighbours;
    }

    //Returns a hashmap with, key = Direction, value = value of adjacent node of the board.
    public Map<Direction, Integer> getValuesOfAdjacentNodes(int[][] board, int x, int y) {
        Map<Direction, Integer> adjacentNodes = new HashMap<>();
        if (x < 3) {
            adjacentNodes.put(Direction.RIGHT, board[y][x + 1]);
        }
        if (y < 3) {
            adjacentNodes.put(Direction.DOWN, board[y + 1][x]);
        }
        if (x > 0) {
            adjacentNodes.put(Direction.LEFT, board[y][x - 1]);
        }
        if (y > 0) {
            adjacentNodes.put(Direction.UP, board[y - 1][x]);
        }
        return adjacentNodes;
    }
}
