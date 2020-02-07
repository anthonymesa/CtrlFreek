import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Scanner;
import javax.swing.*;
import java.awt.event;

public class CtrlFreek extends JFrame
{
    String path =  File(CtrlFreek.class.getProtectionDomain().getCodeSource().getLocation().toURI()).getPath();
    char drive_letter = path.getCharAt(0);

    public static void main(final String args[]) throws IOException{
        this.setSize(300,150);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setTitle("Click Event");

        final JButton choose_directory = new JButton("...");
        final JTextField display_directory = new JTextField();
        final JButton control = new JButton("Control");
        final JRadioButton run = new JRadioButton("Java Run", false);
        final JRadioButton jar = new JRadioButton("Java .jar", false);
        final JRadioButton cpp = new JRadioButton("C++", false);

        final JTextArea terminal = new JTextArea(5, 20);
        final JScrollPane scrollPane = new JScrollPane(terminal); 
        terminal.setEditable(false);

        CallCommand({drive_letter + ":/Compiling_Tools/winCompile/cmake-3.16.0-rc2-win64-x64/bin/cmake.exe", "-B", "bin/win", "-G", "Visual Studio 16 2019"});
    }

    public void CallCommand(final String[] commands) throws IOException
    {
        final Runtime rt = Runtime.getRuntime();
        final Process proc = rt.exec(commands);
        WriteToTerminal(proc);
    }

    public void WriteToTerminal(final Process proc) throws IOException
    {
        final BufferedReader stdInput = new BufferedReader(new 
            InputStreamReader(proc.getInputStream()));

        final BufferedReader stdError = new BufferedReader(new 
            InputStreamReader(proc.getErrorStream()));

        // Read the output from the command
        System.out.println("Here is the standard output of the command:\n");
        String s = null;
        while ((s = stdInput.readLine()) != null) {
            terminal.append(s);
        }

        // Read any errors from the attempted command
        System.out.println("Here is the standard error of the command (if any):\n");
        while ((s = stdError.readLine()) != null) {
            terminal.append(s);
        }
    }
}


// /*
//  * To change this license header, choose License Headers in Project Properties.
//  * To change this template file, choose Tools | Templates
//  * and open the template in the editor.
//  */
// package javafxapplication1;

// import javafx.application.Application;
// import javafx.event.ActionEvent;
// import javafx.event.EventHandler;
// import javafx.geometry.Insets;
// import javafx.geometry.Pos;
// import javafx.scene.Scene;
// import javafx.scene.control.Button;
// import javafx.scene.control.TextArea;
// import javafx.scene.layout.GridPane;
// import javafx.scene.layout.StackPane;
// import javafx.stage.Stage;

// /**
//  *
//  * @author admesa
//  */
// public class JavaFXApplication1 extends Application {
    
//     @Override
//     public void start(Stage primaryStage) {
//         GridPane grid = new GridPane();
//         grid.setAlignment(Pos.CENTER);
//         grid.setHgap(10);
//         grid.setVgap(10);
//         grid.setPadding(new Insets(25, 25, 25, 25));
        
//         Button btn = new Button();
//         btn.setText("Say 'Hello World'");
        
//         grid.add(btn, 0, 0);
        
//         TextArea terminal = new TextArea();
        
//         grid.add(terminal, 0, 1);
        
//         btn.setOnAction(new EventHandler<ActionEvent>() {
            
//             @Override
//             public void handle(ActionEvent event) {
//                 System.out.println("Hello World!");
//                 terminal.setText("Hello World");
//             }
//         });
        
//         Scene scene = new Scene(grid, 300, 550);
        
//         primaryStage.setTitle("Hello World!");
//         primaryStage.setScene(scene);
//         primaryStage.show();
//     }

//     /**
//      * @param args the command line arguments
//      */
//     public static void main(String[] args) {
//         launch(args);
//     }
    
// }
