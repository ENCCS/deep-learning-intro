---
myst:
    substitutions:
        palmer_penguins: |
            ```{figure} _patched/episodes/fig/palmer_penguins.png
            :alt: 'Illustration of the three species of penguins found in the Palmer Archipelago, Antarctica: Chinstrap, Gentoo and Adele'

            "Palmer Penguins"
            ```
        
        penguin_beaks: |
            ```{figure} _patched/episodes/fig/culmen_depth.png
            :alt: 'Illustration of how the beak dimensions were measured. In the raw data, bill dimensions are recorded as "culmen length" and "culmen depth". The culmen is the dorsal ridge atop the bill.'

            "Culmen Depth"
            ```

        pairplot: |
            ```{figure} _patched/episodes/fig/pairplot.png
            :alt: 'Grid of scatter plots and histograms comparing observed values of the four physicial attributes (features) measured in the penguins sampled. Scatter plots illustrate the distribution of values observed for each pair of features. On the diagonal, where one feature would be compared with itself, histograms are displayed that show the distribution of values observed for that feature, coloured according to the species of the individual sampled. The pair plot shows distinct but overlapping clusters of data points representing the different species, with no pair of features providing a clean separation of clusters on its own.'

            "Pair Plot"
            ```

        sex_pairplot: |
            ```{figure} _patched/episodes/fig/02_sex_pairplot.png
            :alt: 'Grid of scatter plots and histograms comparing observed values of the four physicial attributes (features) measured in the penguins sampled, with data points coloured according to the sex of the individual sampled. The pair plot shows similarly-shaped distribution of values observed for each feature in male and female penguins, with the distribution of measurements for females skewed towards smaller values.'
            
            "Pair plot grouped by sex"
            ```

        plot_model: |
            ```{figure} _patched/episodes/fig/02_plot_model.png
            :alt: 'A directed graph showing the three layers of the neural network connected by arrows. First layer is of type InputLayer. Second layer is of type Dense with a relu activation. The third layer is also of type Dense, with a softmax activation. The input and output shapes of every layer are also mentioned. Only the second and third layers contain trainable parameters.'

            "Output of keras.utils.plot_model() function"
            ```

        training_curve: |
            ```{figure} _patched/episodes/fig/02_training_curve.png
            :alt: 'Training loss curve of the neural network training which depicts exponential decrease in loss before a plateau from ~10 epochs'

            "Training Curve"
            ```

        bad_training_curve: |
            ```{figure} _patched/episodes/fig/02_bad_training_history_1.png
            :alt: 'Very jittery training curve with the loss value jumping back and forth between 2 and 4. The range of the y-axis is from 2 to 4, whereas in the previous training curve it was from 0 to 2. The loss seems to decrease a litle bit, but not as much as compared to the previous plot where it dropped to almost 0. The minimum loss in the end is somewhere around 2.'
            
            "Training Curve Gone Wrong"
            ```

        confusion_matrix: |
            ```{figure} _patched/episodes/fig/confusion_matrix.png
            :alt: 'Confusion matrix of the test set with high accuracy for Adelie and Gentoo classification and no correctly predicted Chinstrap'

            "Confusion Matrix"
            ```

---

# 2. Classification by a neural network using Keras

```{include} _patched/episodes/2-keras.md
:relative-docs: _patched/episodes
:relative-images: _patched/episodes
:end-before: [palmer-penguins]: fig/palmer_penguins.png
```

```{include} _patched/episodes/2-keras.md
:relative-docs: _patched/episodes
:relative-images: _patched/episodes
:start-after: and no correctly predicted Chinstrap'}
```
