from cogbooks import strip_text
from hypothesis import given
import hypothesis.strategies as st


@given(
    pre_code_delim=st.characters(),
    code_delim=st.characters(),
    post_code_delim=st.characters(),
    pre_md_delim=st.characters(),
    md_delim=st.characters(),
    post_md_delim=st.characters(),
    pre_note_delim=st.characters(),
    note_delim=st.characters(),
    post_note_delim=st.characters(),
)
def test_combined_rand_text(
    pre_code_delim,
    code_delim,
    post_code_delim,
    pre_md_delim,
    md_delim,
    post_md_delim,
    pre_note_delim,
    note_delim,
    post_note_delim,
):
    text = (
        pre_code_delim
        + "# <COGINST>"
        + code_delim
        + "# </COGINST>"
        + post_code_delim
        + pre_md_delim
        + "<COGINST>"
        + md_delim
        + "</COGINST>"
        + post_md_delim
        + pre_note_delim
        + "<COGNOTE>"
        + note_delim
        + "</COGNOTE>"
        + post_note_delim
    )

    filtered_text = (
        pre_code_delim
        + "# STUDENT CODE HERE"
        + post_code_delim
        + pre_md_delim
        + "*SOLUTION HERE*"
        + post_md_delim
        + pre_note_delim
        + post_note_delim
    )
    assert strip_text(text) == filtered_text


def test_ex_ipynb():
    text = """
    <!-- #region -->
    3.7 Read in the stock market data from `data/dow.txt`. Each data point corresponds to the daily closing value of the Dow Jones Industrial Average (starting in late 2006 and ending in late 2010). Use the following code to read in the data:
    
    ```python
    with open("data/dow.txt", 'r') as R:
        # Each row of the txt file contains the closing value of the market
        # This data is read in as a numpy array of floating point values
        data = np.asarray([float(i) for i in R])
    ```
    
    Plot the data on labeled axes.
    
    <COGNOTE>
    
    #### Instructor Note:
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    
    </COGNOTE>
    <!-- #endregion -->
    
    ```python
    # 3.7 SOLUTION
    # <COGINST>
    with open("data/dow.txt", 'r') as R:
        data = np.asarray([float(i) for i in R])
    
    fig, ax = plt.subplots()
    ax.plot(data)
    ax.grid()
    ax.set_xlabel("Days")
    ax.set_ylabel("Dow Jones Industrial Average");
    # </COGINST>
    ```
    
    3.8 Perform an FFT on this real-valued data, and plot $|c_{k}|$ vs $\nu_{k}$. The y-axis should be on a log scale. The $\nu_{k}$-axis should be scaled to be in units of [1 / days].
    
    ```python
    # <COGINST>
    ck =  np.fft.rfft(data)
    L = len(data)
    k = np.arange(len(ck)) / L
    fig, ax = plt.subplots()
    
    ax.plot(k, np.abs(ck))
    ax.set_xlabel("Frequency [1 / days]")
    ax.set_yscale("log")
    # </COGINST>
    ```
    
    3.9 We want to smooth this stock market data. We can do this by "removing" the high-frequency coefficients of its Fourier spectrum. Try zeroing-out the top 90% high-frequency coefficients, and then perform an inverse FFT using these altered coefficients. Plot the "recovered" signal on top of a semi-transparent version of the original data (use the plot parameter `alpha=0.5`). Then repeat this, but with zeroing out the top 98% coefficients. In both of these cases, on what scale are the fluctuations being filtered out?
    > 3.9 Solution. <COGINST>Filtering out the top 90% of the coefficients removes all of the day-to-day fluctuations, up to the fluctuations over twenty-day spans. Filtering the top 98% coefficients extends this up to 100-day fluctuations.</COGINST>
    
    ```python
    # 3.9 SOLUTION
    # <COGINST>
    ck =  np.fft.rfft(data)
    ck[round(.1 * len(ck)):] = 0
    smooth = np.fft.irfft(ck)
    
    fig, ax = plt.subplots()
    ax.plot(data, alpha=0.5)
    ax.plot(smooth)
    ax.set_xlabel("Days")
    ax.set_ylabel("Dow Jones Industrial Average")
    # </COGINST>
    ```
    
    ```python
    # 3.9 SOLUTION
    # <COGINST>
    ck =  np.fft.rfft(data)
    ck[round(.02 * len(ck)):] = 0
    smooth = np.fft.irfft(ck)
    
    fig, ax = plt.subplots()
    ax.plot(data, alpha=0.5)
    ax.plot(smooth)
    ax.set_xlabel("Days")
    ax.set_ylabel("Dow Jones Industrial Average")
    # </COGINST>
    ```
    """

    filtered_text = """
    <!-- #region -->
    3.7 Read in the stock market data from `data/dow.txt`. Each data point corresponds to the daily closing value of the Dow Jones Industrial Average (starting in late 2006 and ending in late 2010). Use the following code to read in the data:
    
    ```python
    with open("data/dow.txt", 'r') as R:
        # Each row of the txt file contains the closing value of the market
        # This data is read in as a numpy array of floating point values
        data = np.asarray([float(i) for i in R])
    ```
    
    Plot the data on labeled axes.
    
    
    <!-- #endregion -->
    
    ```python
    # 3.7 SOLUTION
    # STUDENT CODE HERE
    ```
    
    3.8 Perform an FFT on this real-valued data, and plot $|c_{k}|$ vs $\nu_{k}$. The y-axis should be on a log scale. The $\nu_{k}$-axis should be scaled to be in units of [1 / days].
    
    ```python
    # STUDENT CODE HERE
    ```
    
    3.9 We want to smooth this stock market data. We can do this by "removing" the high-frequency coefficients of its Fourier spectrum. Try zeroing-out the top 90% high-frequency coefficients, and then perform an inverse FFT using these altered coefficients. Plot the "recovered" signal on top of a semi-transparent version of the original data (use the plot parameter `alpha=0.5`). Then repeat this, but with zeroing out the top 98% coefficients. In both of these cases, on what scale are the fluctuations being filtered out?
    > 3.9 Solution. *SOLUTION HERE*
    
    ```python
    # 3.9 SOLUTION
    # STUDENT CODE HERE
    ```
    
    ```python
    # 3.9 SOLUTION
    # STUDENT CODE HERE
    ```
    """

    assert strip_text(text) == filtered_text
