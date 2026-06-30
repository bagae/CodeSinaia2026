from point import Point

INPUT_FILENAME = "data.txt"
OUTPUT_FILENAME = "data.tsv"

# Check if a point name is valid
def check_valid(point_name):
    """Validate a point name.
    Args:
        point_name: Candidate point name extracted from input.
    Raises:
        ValueError: If the name is purely numeric.
    """
    try:
        int(point_name)
        raise ValueError(f"Invalid Point name ({point_name} must not be numerical)!")
    except ValueError:
        pass

# Parse a Point line
def parse_point(line):
    """Parse one input line into a Point.
    Args:
        line: Text line in the form Point_P24=(x=461, y=185).
    Returns:
        A tuple (success, result). On success, result is a Point. On failure,
        result is an error message string.
    """
    try:
        point_name = line.split("_", 1)[1].split("=", 1)[0]
        check_valid(point_name)
        point_x = int(line.split("x=", 1)[1].split(",", 1)[0])
        point_y = int(line.split("y=", 1)[1].split(")", 1)[0])
        return True, Point(point_name, point_x, point_y)
    except (IndexError, ValueError) as e:
        return False, f"Point {point_name}: {str(e)}"

# Read the input
def read_points(filename):
    """Read and parse all points from an input text file.
    Args:
        filename: Path to the input file.
    Returns:
        A tuple (points, errors). points is a list of Point objects when the
        file is available, otherwise None. errors is a list of error messages.
    """
    points = []
    errors = []
    line_number = 0
    f = None
    try:
        f = open(filename, encoding="utf-8")
        for line in f:
            line_number += 1
            # a line looks like 'Point_P16=(x=-196, y=209)'
            # need to extract the name (in between _ and first =) and each of the x= and y= coordinates
            success, arg = parse_point(line.strip())
            if type(arg) is Point:
                points.append(arg)
            else:
                errors.append(f"Line {line_number}: {arg}")
        return points, errors
    except FileNotFoundError:
        return None, [f"File {filename} was not found!"]
    finally:
        if f: 
            f.close()

# Write the output
def write_points(points, filename):
    """Write points to a TSV file with Name, X, Y columns.
    Args:
        points: List of Point objects to write.
        filename: Output TSV file path.
    """
    with open(filename, "w", encoding="utf-8", newline="") as f:
        f.write(f"Name\tX\tY\n")
        for point in points:
            f.write(f"{point._name}\t{point._x}\t{point._y}\n")

# Pipeline runner: Data transformation from txt to tsv
def run(input, output):
    """Transform point data from text format into TSV format.
    Args:
        input: Path to the input text file containing lines like
            Point_P24=(x=461, y=185)
        output: Path to the output TSV file to generate.
    Returns:
        A list of log lines. The first line is a summary and the following
        lines (if any) are parsing errors.
    """
    points, errors = read_points(input)
    log = [f"Loaded {len(points) if points else 0}. Failed parsing {len(errors) if errors else 0}."]
    if errors:
        log.extend(errors)
    write_points(points, output)
    return log

if __name__ == "__main__":
    log = run(INPUT_FILENAME, OUTPUT_FILENAME)
    print(*log, sep="\n")
