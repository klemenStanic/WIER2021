

# Road Runner
Overview:
1) Clean the data 
   1) Retain only body
   2) Remove \n, \t, \r
   3) Remove scripts
   4) Other 
2) Create a list of tokens for both the Wrapper and Sample -> custom parser
3) 
```
wrapper_index, sample_index = 0                                                                       # initialize indexes
while wrapper_index is not equal to wrapper.length and sample_index is not equal to sample.length:    # run until the end of either the wrapper or sample
    sample_element = sample[sample_index]
    wrapper_element = wrapper[sample_index]
    
    if sample_element is equal to wrapper_element:                                                    # check for tag mismatch, if the elements match, we continue 
        wrapper_index, sample_index ++                                                                # increment indexes
        continue

                                                                                                      # elements do not match, we could have a string mismatch
                                                                                                      # or we have a tag mismatch, which could represent a iterator
                                                                                                      # or an optional element, 
    
    if sample_element is not a tag and wrapper_element is not a tag:
        Mark the element in the wrapper as a #TEXT
    
                                                                                                      # from here on, we either stumbled upon an optional element,
                                                                                                      # or an iterator. We first check whether the element is an iterator,
                                                                                                      # if its not, it must be an optional element.
    if find_the_iterator returns false:
        find_the_optional
```

