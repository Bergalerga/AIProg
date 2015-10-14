package org.ntnu.it3105.game;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.PriorityQueue;

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

    private float expectimax(int[][] board, int depth, boolean maximizing_player) {
        if (depth == 0) {
            int h = heuristic(board);
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


    public int heuristic(int[][] board) {
        //TALE PLS

        double[][] gradient = {
                { 7, 6, 5, 4 },
                { 6, 4, 3, 3 },
                { 5, 3, 2, 2 },
                { 4, 3, 2, 1 }
        };
        int h = 0;

        for (int x = 0; x < 4; x++) {
            for (int y = 0; y < 4; y++) {
                if (board[x][y] == 0) {
                    h += 1;
                }
                h += board[x][y];
                h += board[x][y]*gradient[x][y];
            }
        }

        return h;
        //END TALE PLS
    }

    public ArrayList<int[][]> getNeighbours(int[][] board) {
        ArrayList<int[][]> neighbours = new ArrayList();
        for (Direction dir : Direction.values()) {
            neighbours.add(Board.checkMove(board, dir));
        }
        return neighbours;
    }
}
