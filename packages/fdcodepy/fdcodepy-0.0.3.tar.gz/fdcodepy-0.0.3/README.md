# fdcodepy

## Introduction

- FD_codepy is an open-source python package that can be used to extract time series in an interpretable manner, and use it for compression.
- The key idea is proposed specifically for metered data in energy sector, but can also be used with smart sensors and edge computing.
- Inspired by Codebook method, it breaks down the time series data into its constituent parts, i.e., the unique sub-patterns called Codewords, and the index of the Codewords, i.e., representations, allowing for efficient compression and analysis.
- Compared to resampling data into lower resolution, this lossy compression method takes similar data storage and transmission bandwidth, while preserving high frequency information and accumulative/average metered values.

The FD_codepy source code is on GitHub: https://github.com/abc123yuanrui/FD_codepy/

## Key method for time series compression

- Flexbility distance: a novel distance metric that measures the similarity between time series data while taking into account both temporal and amplitude distance, and the rebound effect of the data.

## Installation

- Install using pip: `pip install fdcodepy`

## Usage

- Import the package: `import fdcodepy`
- Codebook compression for a given hourly time series and window size of 24, which decides the compression ratio (same with resmpling data from hourly into daily)
  - `from fdcodepy import methods`
  - `sample_series = np.random.uniform(0, 30, 365*24)`
  - `series_codebook = methods.Code_book(time_series, 24, 'flexibilityD')`
  - `series_codebook.pre_processing()`
  - `distance_matrix, quantiles = series_codebook.get_distance_matrix()`
  - `codewords, representations = series_codebook.desolve_time_series_thre(quantiles[1])`
  - `series_codebook.post_processing()`
- The representations are the length of data needs to be communicated to data center, which is equal to the size of downsampled data, in this case, 365
- Use the `FlexibilityDistance` to compute the flexibility distance between two time series datasets (with default settings).
  - `from fdcodepy import methods`
  - `Code_book.flex_distance(time_series_1, time_series_2)`
