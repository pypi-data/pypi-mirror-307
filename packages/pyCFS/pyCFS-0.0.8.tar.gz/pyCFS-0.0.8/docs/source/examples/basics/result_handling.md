## Result handling

### Results

The main results are the results which are obtained from the *hdf* file produced by `openCFS` after a successful simulation. These results are stored internally into the `results` field and are of type `List[nestedResultDict]`. To allow an easier acquisition of the tracked results there are a few functions which provide useful options. 

### History results

History results from `openCFS` which are usually written to *.hist* files (just normal *txt* files) can also be written to the main *hdf* results file. 

:::{important}
`pyCFS` only handles history results which are saved to the main *hdf* results file.
:::

To set this up in your *xml* simulation file you just have to do the following. At the beginning of the file we need to add an output identifier for *hdf* files. 

```xml
<fileFormats>
    <!-- ... -->
    <output>
        <hdf5 id="hdf"/>
    </output>
    <!-- ... -->
</fileFormats>
```

Then we can define the history results as usual with the only difference being that we also specify `outputIds="hdf"`. 

```xml
<!-- Example calculating electrical energy in all regions -->
<regionResult type="elecEnergy">
    <allRegions outputIds="hdf"/>
</regionResult>
```

This way the history results will be written to the main *hdf* results file instead of the *.hist* files. 

The read history results are internally saved into `hist_results` which is a list of nested dictionaries `List[nestedResultDict]`.