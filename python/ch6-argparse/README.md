# 类图生成

安装pylint
```
pip install pylint
```
查看 `pyreverse` 命令 
```
pyreverse -h         
Usage: 
  pyreverse [options] <packages>

  create UML diagrams for classes and modules in <packages>


Options:
  -h, --help            show this help message and exit
  -f <mode>, --filter-mode=<mode>
                        filter attributes and functions according to
                        <mode>. Correct modes are :
                        'PUB_ONLY' filter all non public attributes
                        [DEFAULT], equivalent to PRIVATE+SPECIAL_A
                        'ALL' no filter                             'SPECIAL'
                        filter Python special functions
                        except constructor                             'OTHER'
                        filter protected and private
                        attributes [current: PUB_ONLY]
  -c <class>, --class=<class>
                        create a class diagram with all classes related to
                        <class>; this uses by default the options -ASmy
                        [current: none]
  -a <ancestor>, --show-ancestors=<ancestor>
                        show <ancestor> generations of ancestor classes not in
                        <projects>
  -A, --all-ancestors   show all ancestors off all classes in <projects>
  -s <association_level>, --show-associated=<association_level>
                        show <association_level> levels of associated classes
                        not in <projects>
  -S, --all-associated  show recursively all associated off all associated
                        classes
  -b, --show-builtin    include builtin objects in representation of classes
  -m [yn], --module-names=[yn]
                        include module name in representation of classes
  -k, --only-classnames
                        don't show attributes and methods in the class boxes;
                        this disables -f values
  -o <format>, --output=<format>
                        create a *.<format> output file if format available.
                        [current: dot]
  --ignore=<file[,file...]>
                        Add files or directories to the blacklist. They should
                        be base names, not paths. [current: CVS]
  -p <project name>, --project=<project name>
                        set the project name. [current: none]
```
生成类图:
```
pyreverse argparse -o png
```

```
dot -Tpng classes.dot -o c.png
```

```
pyreverse -k -m y  ./   
# package.dot
```