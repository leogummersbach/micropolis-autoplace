## Custom connection convention

Custom connections can use any character for specifying a type of structure that should connect to another module.
Setting up different types of custom connection, one can easily loose control about what represents what.
Therefore, it is useful to set up a convention clarifying what a character represents in the model.

<table>
    <thead>
        <tr>
          <th>ascii value (dec)</th>
          <th>character</th>
          <th>description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
          <td>82</td>
          <td>R</td>
          <td>Railway (elevated, railway tiles are placed 5 plates above the main plate)</td>
        </tr>
        <tr>
          <td>83</td>
          <td>S</td>
          <td>Street</td>
        </tr>
        <tr>
          <td>84</td>
          <td>T</td>
          <td>Train station (major, with roof)</td>
        </tr>
	    <tr>
          <td>87</td>
          <td>W</td>
          <td>Water</td>
        </tr>
        <tr>
          <td>114</td>
          <td>r</td>
          <td>Railway on ground level</td>
        </tr>
        <tr>
          <td>115</td>
          <td>s</td>
          <td>Subway (railway line which lays beneath the ground level, usually without roof (like a ditch))</td>
        </tr>
        <tr>
          <td>116</td>
          <td>t</td>
          <td>Train station (minor, without roof)</td>
        </tr>
        <tr>
          <td>119</td>
          <td>w</td>
          <td>Wall (Party wall of a building)</td>
        </tr>
    </tbody>
</table>