import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.util.Random;

public class GuessingGameApp extends JFrame {

    private final Random random = new Random();

    // State Variables
    private int maxRange = 100;
    private int maxAttempts = 7;
    private int targetNumber;
    private int attemptsUsed = 0;
    private int totalScore = 0;
    private int currentRound = 1;

    // UI Components
    private JComboBox<String> difficultyBox;
    private JTextField guessField;
    private JButton guessButton;
    private JButton playAgainButton;
    private JLabel feedbackLabel;
    private JLabel attemptsLabel;
    private JLabel scoreLabel;
    private JLabel rangeLabel;

    public GuessingGameApp() {
        setTitle("Number Guessing Game - Oasis Infobyte");
        setSize(480, 420);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setResizable(false);

        initUI();
        startNewRound();
    }

    private void initUI() {
        JPanel mainPanel = new JPanel(new BorderLayout(15, 15));
        mainPanel.setBorder(new EmptyBorder(20, 25, 20, 25));
        mainPanel.setBackground(new Color(245, 247, 250));

        // Header Panel
        JPanel headerPanel = new JPanel(new GridLayout(2, 1, 5, 5));
        headerPanel.setBackground(new Color(245, 247, 250));

        JLabel titleLabel = new JLabel("Number Guessing Game", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 22));
        titleLabel.setForeground(new Color(33, 37, 41));
        headerPanel.add(titleLabel);

        JPanel settingsPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 0));
        settingsPanel.setBackground(new Color(245, 247, 250));
        JLabel diffLabel = new JLabel("Difficulty:");
        diffLabel.setFont(new Font("Segoe UI", Font.PLAIN, 14));

        String[] levels = {"Easy (1 - 50, 10 Tries)", "Medium (1 - 100, 7 Tries)", "Hard (1 - 200, 5 Tries)"};
        difficultyBox = new JComboBox<>(levels);
        difficultyBox.setSelectedIndex(1); // Medium default
        difficultyBox.addActionListener(e -> {
            updateDifficultySettings();
            startNewRound();
        });

        settingsPanel.add(diffLabel);
        settingsPanel.add(difficultyBox);
        headerPanel.add(settingsPanel);
        mainPanel.add(headerPanel, BorderLayout.NORTH);

        // Center Action Panel
        JPanel centerPanel = new JPanel(new GridLayout(4, 1, 10, 10));
        centerPanel.setBackground(new Color(245, 247, 250));

        rangeLabel = new JLabel("Guess a number between 1 and 100", SwingConstants.CENTER);
        rangeLabel.setFont(new Font("Segoe UI", Font.PLAIN, 15));
        centerPanel.add(rangeLabel);

        JPanel inputPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 0));
        inputPanel.setBackground(new Color(245, 247, 250));
        guessField = new JTextField(8);
        guessField.setFont(new Font("Segoe UI", Font.BOLD, 18));
        guessField.setHorizontalAlignment(JTextField.CENTER);

        guessButton = new JButton("Submit Guess");
        guessButton.setFont(new Font("Segoe UI", Font.BOLD, 14));
        guessButton.setBackground(new Color(13, 110, 253));
        guessButton.setForeground(Color.WHITE);
        guessButton.setFocusPainted(false);
        guessButton.addActionListener(this::handleGuess);
        guessField.addActionListener(this::handleGuess);

        inputPanel.add(guessField);
        inputPanel.add(guessButton);
        centerPanel.add(inputPanel);

        feedbackLabel = new JLabel("Take your first guess!", SwingConstants.CENTER);
        feedbackLabel.setFont(new Font("Segoe UI", Font.BOLD, 16));
        feedbackLabel.setForeground(new Color(108, 117, 125));
        centerPanel.add(feedbackLabel);

        attemptsLabel = new JLabel("Attempts: 0 / 7", SwingConstants.CENTER);
        attemptsLabel.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        centerPanel.add(attemptsLabel);

        mainPanel.add(centerPanel, BorderLayout.CENTER);

        // Footer Score & Reset Panel
        JPanel footerPanel = new JPanel(new BorderLayout(10, 10));
        footerPanel.setBackground(new Color(245, 247, 250));

        scoreLabel = new JLabel("Round: 1  |  Score: 0 pts", SwingConstants.LEFT);
        scoreLabel.setFont(new Font("Segoe UI", Font.BOLD, 14));
        scoreLabel.setForeground(new Color(25, 135, 84));
        footerPanel.add(scoreLabel, BorderLayout.WEST);

        playAgainButton = new JButton("Play Again");
        playAgainButton.setFont(new Font("Segoe UI", Font.BOLD, 13));
        playAgainButton.setBackground(new Color(108, 117, 125));
        playAgainButton.setForeground(Color.WHITE);
        playAgainButton.setFocusPainted(false);
        playAgainButton.setEnabled(false);
        playAgainButton.addActionListener(e -> {
            currentRound++;
            startNewRound();
        });
        footerPanel.add(playAgainButton, BorderLayout.EAST);

        mainPanel.add(footerPanel, BorderLayout.SOUTH);

        add(mainPanel);
    }

    private void updateDifficultySettings() {
        int idx = difficultyBox.getSelectedIndex();
        if (idx == 0) {
            maxRange = 50;
            maxAttempts = 10;
        } else if (idx == 2) {
            maxRange = 200;
            maxAttempts = 5;
        } else {
            maxRange = 100;
            maxAttempts = 7;
        }
        rangeLabel.setText(String.format("Guess a number between 1 and %d", maxRange));
    }

    private void startNewRound() {
        updateDifficultySettings();
        targetNumber = random.nextInt(maxRange) + 1;
        attemptsUsed = 0;

        guessField.setText("");
        guessField.setEnabled(true);
        guessButton.setEnabled(true);
        playAgainButton.setEnabled(false);
        difficultyBox.setEnabled(true);

        feedbackLabel.setText("Take your first guess!");
        feedbackLabel.setForeground(new Color(108, 117, 125));
        updateStatusBar();
        guessField.requestFocusInWindow();
    }

    private void handleGuess(ActionEvent e) {
        String input = guessField.getText().trim();
        int guess;

        try {
            guess = Integer.parseInt(input);
        } catch (NumberFormatException ex) {
            feedbackLabel.setText("Invalid! Enter a valid integer.");
            feedbackLabel.setForeground(new Color(220, 53, 69));
            return;
        }

        if (guess < 1 || guess > maxRange) {
            feedbackLabel.setText(String.format("Out of bounds! (1 to %d)", maxRange));
            feedbackLabel.setForeground(new Color(220, 53, 69));
            return;
        }

        attemptsUsed++;
        difficultyBox.setEnabled(false);

        if (guess == targetNumber) {
            int roundScore = (maxAttempts - attemptsUsed + 1) * 10;
            totalScore += roundScore;
            feedbackLabel.setText(String.format("Correct! Won in %d attempts (+%d pts)!", attemptsUsed, roundScore));
            feedbackLabel.setForeground(new Color(25, 135, 84));
            finishRound();
        } else if (attemptsUsed >= maxAttempts) {
            feedbackLabel.setText(String.format("You Lost! The number was %d.", targetNumber));
            feedbackLabel.setForeground(new Color(220, 53, 69));
            finishRound();
        } else if (guess < targetNumber) {
            feedbackLabel.setText("Too Low!");
            feedbackLabel.setForeground(new Color(253, 126, 20));
        } else {
            feedbackLabel.setText("Too High!");
            feedbackLabel.setForeground(new Color(13, 110, 253));
        }

        updateStatusBar();
        guessField.selectAll();
        guessField.requestFocusInWindow();
    }

    private void finishRound() {
        guessField.setEnabled(false);
        guessButton.setEnabled(false);
        playAgainButton.setEnabled(true);
        difficultyBox.setEnabled(true);
    }

    private void updateStatusBar() {
        attemptsLabel.setText(String.format("Attempts: %d / %d", attemptsUsed, maxAttempts));
        scoreLabel.setText(String.format("Round: %d  |  Score: %d pts", currentRound, totalScore));
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            GuessingGameApp app = new GuessingGameApp();
            app.setVisible(true);
        });
    }
}