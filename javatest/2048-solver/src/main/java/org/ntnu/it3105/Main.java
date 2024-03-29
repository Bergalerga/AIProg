package org.ntnu.it3105;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;
import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Logger;
import org.ntnu.it3105.game.AI;
import org.ntnu.it3105.game.Controller;
import org.ntnu.it3105.game.Direction;
import java.io.IOException;

public class Main extends Application {

    private static final Logger log = Logger.getLogger(Main.class);

    private Stage primaryStage;
    private Scene scene;
    private AnchorPane root;
    private Controller controller;
    private AI ai;

    @Override
    public void start(Stage primaryStage) {
        log.info("Starting 2048 JavaFX application");

        BasicConfigurator.configure();
        this.primaryStage = primaryStage;

        loadBoardAndSetScene();
        configureAndShowPrimaryStage();

        //Initialize the ai
        ai = new AI(4);

        // Setting global key listener for the scene
        scene.setOnKeyReleased((keyEvent) -> {

            switch (keyEvent.getCode()) {
                case S:
                    log.info("Use AI to solve the game");
                    while(1<2){

                        controller.doMove(ai.getNextMove(controller.getBoard()));
                    }
                case ENTER:
                    log.info("Use AI to do one move");
                    controller.doMove(ai.getNextMove(controller.getBoard()));

                    break;
                default:
                    try {
                        controller.doMove(Direction.directionFor(keyEvent.getCode()));
                    } catch (IllegalArgumentException e) {
                        log.debug("The user entered an invalid key code for direction: " + keyEvent.getCode());
                    }
                    break;
            }

        });
    }

    /**
     * Method for configuring the primaryStage
     */
    private void configureAndShowPrimaryStage() {
        primaryStage.setResizable(false);
        primaryStage.setTitle("2048-solver");
        primaryStage.show();
    }

    /**
     * Method for loading the board-fxml file and populating the scene and primaryStage
     */
    private void loadBoardAndSetScene() {
        log.info("Loading Board.fxml onto primaryStage");
        FXMLLoader loader = new FXMLLoader();
        loader.setLocation(getClass().getClassLoader().getResource("fxml/Board.fxml"));

        try {
            root = loader.load();
            controller  = loader.getController();
        } catch (IOException e) {
            e.printStackTrace();
        }

        scene = new Scene(root);
        scene.getStylesheets().add("css/stylesheet.css");
        this.primaryStage.setScene(scene);
    }

    /**
     * Returns the main stage.
     * @return
     */
    public Stage getPrimaryStage() {
        return primaryStage;
    }

    /**
     * Main method
     * @param args
     */
    public static void main( String[] args ) {
        launch(args);
    }
}
