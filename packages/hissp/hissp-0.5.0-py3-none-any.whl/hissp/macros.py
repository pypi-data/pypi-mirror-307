("Hissp's bundled `tag` and `macro` metaprograms.\n"
 '\n'
 'While completely optional, these bring Hissp up to a minimal standard of\n'
 'practical utility without adding dependencies. As a convenience, they\n'
 'are automatically made available `unqualified` in the Lissp `REPL`, but\n'
 'this is not true of modules.\n'
 '\n'
 "Hissp's `standalone property` means the compiled output of code written\n"
 'using these metaprograms need not have Hissp installed at run time to\n'
 'work, only the Python standard library. All helper code must therefore\n'
 'be inlined, resulting in larger expansions than might otherwise be\n'
 'necessary.\n'
 '\n'
 'They also have no prerequisite initialization, beyond what is available\n'
 'in a standard Python module. For example, a ``_macro_`` namespace need\n'
 "not be available for ``defmacro``. It's smart enough to check for the\n"
 'presence of ``_macro_`` (at compile time) in its expansion context, and\n'
 'inline the initialization code when required.\n'
 '\n'
 'With the exception of `mix`, which is a `text macro` specifically made\n'
 'for creating a `Python injection`, the other metaprograms eschew\n'
 'expansions of any of their arguments to a `Python injection` (other than\n'
 'the `standard` `symbol` or `string literal fragment` cases), relying\n'
 'only on the built-in special forms ``quote`` and ``lambda``, which makes\n'
 'their expansions compatible with advanced rewriting macros that process\n'
 'the Hissp expansions of other macros.\n'
 '\n'
 '(The -``[#`` and `my# <myQzHASH_>` tags are also something of an\n'
 'exception, as one argument is written in Python to begin with.)\n'
 '\n'
 "That only goes for arguments and doesn't apply to inlined helper\n"
 "functions in the expansions that contain no user code, because that's no\n"
 'worse than using an opaque name imported from somewhere else. `if-else\n'
 '<ifQzH_else>` is one such example, expanding to a lambda containing an\n'
 'injected `conditional expression <if_expr>`, that is called immediately.\n')

globals().update(
  _macro_=__import__('types').SimpleNamespace(
            __doc__=("Hissp's bundled tag and macro namespace.\nSee `hissp.macros`.\n")))

setattr(
  _macro_,
  'defmacro',
  (lambda name, parameters, docstring, *body:
      (
        (
          'lambda',
          (
            ':',
            '_Qzew72czym__G',
            (
              'lambda',
              parameters,
              *body,
              ),
            ),
          (
            'builtins..setattr',
            '_Qzew72czym__G',
            (
              'quote',
              '__doc__',
              ),
            docstring,
            ),
          (
            'builtins..setattr',
            'hissp.macros.._macro_',
            (
              'quote',
              name,
              ),
            '_Qzew72czym__G',
            ),
          (
            'builtins..setattr',
            '_Qzew72czym__G',
            (
              'quote',
              '__code__',
              ),
            (
              '.replace',
              '_Qzew72czym__G.__code__',
              ':',
              'hissp.macros..co_name',
              (
                'quote',
                name,
                ),
              ),
            ),
          (
            'builtins..setattr',
            '_Qzew72czym__G',
            (
              'quote',
              '__name__',
              ),
            (
              'quote',
              name,
              ),
            ),
          (
            'builtins..setattr',
            '_Qzew72czym__G',
            (
              'quote',
              '__qualname__',
              ),
            (
              '.join',
              "('.')",
              (
                'quote',
                (
                  '_macro_',
                  name,
                  ),
                ),
              ),
            ),
          ),
        )
  ))

# defmacro
(
 lambda _Qzew72czym__G=(lambda test, consequent, alternate:
            (
              (
                'lambda',
                'bca',
                'c()if b else a()',
                ),
              test,
              (
                'lambda',
                ':',
                consequent,
                ),
              (
                'lambda',
                ':',
                alternate,
                ),
              )
        ):
   (__import__('builtins').setattr(
      _Qzew72czym__G,
      '__doc__',
      ('``if-else`` Basic ternary branching construct.\n'
       '\n'
       "  Like Python's conditional expressions, the 'else' clause is required.\n"
       '\n'
       '  .. code-block:: REPL\n'
       '\n'
       "     #> (any-map c 'ab\n"
       "     #..  (if-else (op#eq c 'b)                 ;ternary conditional\n"
       "     #..    (print 'Yes)\n"
       "     #..    (print 'No)))\n"
       '     >>> # anyQzH_map\n'
       "     ... __import__('builtins').any(\n"
       "     ...   __import__('builtins').map(\n"
       '     ...     (lambda c:\n'
       '     ...         # ifQzH_else\n'
       '     ...         (lambda b, c, a: c()if b else a())(\n'
       "     ...           __import__('operator').eq(\n"
       '     ...             c,\n'
       "     ...             'b'),\n"
       '     ...           (lambda :\n'
       '     ...               print(\n'
       "     ...                 'Yes')\n"
       '     ...           ),\n'
       '     ...           (lambda :\n'
       '     ...               print(\n'
       "     ...                 'No')\n"
       '     ...           ))\n'
       '     ...     ),\n'
       "     ...     'ab'))\n"
       '     No\n'
       '     Yes\n'
       '     False\n'
       '\n'
       '  See also: `when`, `cond`, `any-map <anyQzH_map>`, `if_expr`.\n'
       '  ')),
    __import__('builtins').setattr(
      __import__('builtins').globals()['_macro_'],
      'ifQzH_else',
      _Qzew72czym__G),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__code__',
      _Qzew72czym__G.__code__.replace(
        co_name='ifQzH_else')),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__name__',
      'ifQzH_else'),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'ifQzH_else',))))  [-1]
)()

# defmacro
(
 lambda _Qzew72czym__G=(lambda *body:
            (
              (
                'lambda',
                ':',
                *body,
                ),
              )
        ):
   (__import__('builtins').setattr(
      _Qzew72czym__G,
      '__doc__',
      ('Evaluates each body expression in sequence (for side effects),\n'
       '  resulting in the value of the last (or ``()`` if empty).\n'
       '\n'
       '  .. code-block:: REPL\n'
       '\n'
       '     #> (print (progn (print 1)                 ;Sequence for side effects, '
       'eval to last.\n'
       '     #..              (print 2)\n'
       '     #..              3))\n'
       '     >>> print(\n'
       '     ...   # progn\n'
       '     ...   (print(\n'
       '     ...      (1)),\n'
       '     ...    print(\n'
       '     ...      (2)),\n'
       '     ...    (3))  [-1])\n'
       '     1\n'
       '     2\n'
       '     3\n'
       '\n'
       '  See also: `prog1`, `Expression statements <exprstmts>`.\n'
       '  ')),
    __import__('builtins').setattr(
      __import__('builtins').globals()['_macro_'],
      'progn',
      _Qzew72czym__G),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__code__',
      _Qzew72czym__G.__code__.replace(
        co_name='progn')),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__name__',
      'progn'),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'progn',))))  [-1]
)()

# defmacro
(
 lambda _Qzew72czym__G=(lambda pairs, *body:
            (
              (
                'lambda',
                (
                  ':',
                  *pairs,
                  ),
                *body,
                ),
              )
        ):
   (__import__('builtins').setattr(
      _Qzew72czym__G,
      '__doc__',
      ('Creates local variables. Pairs are implied by position.\n'
       '\n'
       '  Locals are not in scope until the body.\n'
       '\n'
       '  .. code-block:: REPL\n'
       '\n'
       "     #> (let (x 'a                              ;Create locals.\n"
       "     #..      y 'b)                             ;Any number of pairs.\n"
       '     #..  (print x y)\n'
       "     #..  (let (x 'x\n"
       '     #..        y (op#concat x x))              ;Not in scope until body.\n'
       '     #..    (print x y))                        ;Outer variables shadowed.\n'
       '     #..  (print x y))                          ;Inner went out of scope.\n'
       '     >>> # let\n'
       '     ... (\n'
       "     ...  lambda x='a',\n"
       "     ...         y='b':\n"
       '     ...    (print(\n'
       '     ...       x,\n'
       '     ...       y),\n'
       '     ...     # let\n'
       '     ...     (\n'
       "     ...      lambda x='x',\n"
       "     ...             y=__import__('operator').concat(\n"
       '     ...               x,\n'
       '     ...               x):\n'
       '     ...         print(\n'
       '     ...           x,\n'
       '     ...           y)\n'
       '     ...     )(),\n'
       '     ...     print(\n'
       '     ...       x,\n'
       '     ...       y))  [-1]\n'
       '     ... )()\n'
       '     a b\n'
       '     x aa\n'
       '     a b\n'
       '\n'
       '  See also: `let-from <letQzH_from>`, `my# <myQzHASH_>`, `locals`.\n'
       '  ')),
    __import__('builtins').setattr(
      __import__('builtins').globals()['_macro_'],
      'let',
      _Qzew72czym__G),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__code__',
      _Qzew72czym__G.__code__.replace(
        co_name='let')),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__name__',
      'let'),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'let',))))  [-1]
)()

# defmacro
(
 lambda _Qzew72czym__G=(lambda names, iterable, *body:
            (
              (
                'lambda',
                names,
                *body,
                ),
              ':',
              ':*',
              iterable,
              )
        ):
   (__import__('builtins').setattr(
      _Qzew72czym__G,
      '__doc__',
      ('``let-from`` Create listed locals from iterable.\n'
       '\n'
       '  .. code-block:: REPL\n'
       '\n'
       "     #> (let-from (a b : :* cs) 'ABCDEFG\n"
       '     #..  (print cs b a))\n'
       '     >>> # letQzH_from\n'
       '     ... (lambda a, b, *cs:\n'
       '     ...     print(\n'
       '     ...       cs,\n'
       '     ...       b,\n'
       '     ...       a)\n'
       '     ... )(\n'
       "     ...   *'ABCDEFG')\n"
       "     ('C', 'D', 'E', 'F', 'G') B A\n"
       '\n'
       '  See also: `let`, `let*from <letQzSTAR_from>`, `assignment`.\n'
       '  ')),
    __import__('builtins').setattr(
      __import__('builtins').globals()['_macro_'],
      'letQzH_from',
      _Qzew72czym__G),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__code__',
      _Qzew72czym__G.__code__.replace(
        co_name='letQzH_from')),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__name__',
      'letQzH_from'),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'letQzH_from',))))  [-1]
)()

# defmacro
(
 lambda _Qzew72czym__G=(lambda pairs, *body:
            # ifQzH_else
            (lambda b, c, a: c()if b else a())(
              pairs,
              (lambda :
                  (
                    'hissp.macros.._macro_.letQzH_from',
                    pairs[0],
                    pairs[1],
                    (
                      'hissp.macros..QzMaybe_.letQzSTAR_from',
                      pairs[2:],
                      *body,
                      ),
                    )
              ),
              (lambda :
                  (
                    'hissp.macros.._macro_.progn',
                    *body,
                    )
              ))
        ):
   (__import__('builtins').setattr(
      _Qzew72czym__G,
      '__doc__',
      ("``let*from`` 'let star from' Nested `let-from <letQzH_from>`.\n"
       '\n'
       '  Can unpack nested iterables by using multiple stages.\n'
       '\n'
       '  .. code-block:: REPL\n'
       '\n'
       "     #> (dict : A 'B  C 'D)\n"
       '     >>> dict(\n'
       "     ...   A='B',\n"
       "     ...   C='D')\n"
       "     {'A': 'B', 'C': 'D'}\n"
       '\n'
       '     #> (let*from ((ab cd) (.items _)           ;Nested let-froms.\n'
       "     #..           (a b) ab                     ;Unpacks first item ('A', "
       "'B')\n"
       "     #..           (c d) cd)                    ;Unpacks second item ('C', "
       "'D')\n"
       '     #..  (print a b c d))\n'
       '     >>> # letQzSTAR_from\n'
       '     ... # hissp.macros.._macro_.letQzH_from\n'
       '     ... (lambda ab, cd:\n'
       '     ...     # hissp.macros..QzMaybe_.letQzSTAR_from\n'
       '     ...     # hissp.macros.._macro_.letQzH_from\n'
       '     ...     (lambda a, b:\n'
       '     ...         # hissp.macros..QzMaybe_.letQzSTAR_from\n'
       '     ...         # hissp.macros.._macro_.letQzH_from\n'
       '     ...         (lambda c, d:\n'
       '     ...             # hissp.macros..QzMaybe_.letQzSTAR_from\n'
       '     ...             # hissp.macros.._macro_.progn\n'
       '     ...             print(\n'
       '     ...               a,\n'
       '     ...               b,\n'
       '     ...               c,\n'
       '     ...               d)\n'
       '     ...         )(\n'
       '     ...           *cd)\n'
       '     ...     )(\n'
       '     ...       *ab)\n'
       '     ... )(\n'
       '     ...   *_.items())\n'
       '     A B C D\n'
       '\n'
       '\n'
       '     #> (let*from ((ab cd) (.items _)           ;Fewer stack frames.\n'
       '     #..           (a b c d) `(,@ab ,@cd))      ;Leveraging ,@ splicing.\n'
       '     #..  (print a b c d))\n'
       '     >>> # letQzSTAR_from\n'
       '     ... # hissp.macros.._macro_.letQzH_from\n'
       '     ... (lambda ab, cd:\n'
       '     ...     # hissp.macros..QzMaybe_.letQzSTAR_from\n'
       '     ...     # hissp.macros.._macro_.letQzH_from\n'
       '     ...     (lambda a, b, c, d:\n'
       '     ...         # hissp.macros..QzMaybe_.letQzSTAR_from\n'
       '     ...         # hissp.macros.._macro_.progn\n'
       '     ...         print(\n'
       '     ...           a,\n'
       '     ...           b,\n'
       '     ...           c,\n'
       '     ...           d)\n'
       '     ...     )(\n'
       '     ...       *(\n'
       '     ...          *ab,\n'
       '     ...          *cd,\n'
       '     ...          ))\n'
       '     ... )(\n'
       '     ...   *_.items())\n'
       '     A B C D\n'
       '\n'
       '\n'
       "     #> (let-from (a c b d) ; Didn't really need let*from this time.\n"
       '     #..          `(,@(.keys _) ,@(.values _)) ; Not always this easy.\n'
       '     #..  (print a b c d))\n'
       '     >>> # letQzH_from\n'
       '     ... (lambda a, c, b, d:\n'
       '     ...     print(\n'
       '     ...       a,\n'
       '     ...       b,\n'
       '     ...       c,\n'
       '     ...       d)\n'
       '     ... )(\n'
       '     ...   *(\n'
       '     ...      *_.keys(),\n'
       '     ...      *_.values(),\n'
       '     ...      ))\n'
       '     A B C D\n'
       '\n'
       '  See also: `my# <myQzHASH_>`, `destruct-> <destructQzH_QzGT_>`.\n'
       '  ')),
    __import__('builtins').setattr(
      __import__('builtins').globals()['_macro_'],
      'letQzSTAR_from',
      _Qzew72czym__G),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__code__',
      _Qzew72czym__G.__code__.replace(
        co_name='letQzSTAR_from')),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__name__',
      'letQzSTAR_from'),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'letQzSTAR_from',))))  [-1]
)()

# defmacro
(
 lambda _Qzew72czym__G=(
         lambda qualname,
                params,
                maybeQzH_docstring=(),
                *body:
            # letQzSTAR_from
            # hissp.macros.._macro_.letQzH_from
            (lambda name, *_xs:
                # hissp.macros..QzMaybe_.letQzSTAR_from
                # hissp.macros.._macro_.letQzH_from
                (lambda top, doc:
                    # hissp.macros..QzMaybe_.letQzSTAR_from
                    # hissp.macros.._macro_.progn
                    (
                      'hissp.macros.._macro_.let',
                      (
                        '_Qzwfz72h4o__lambda',
                        (
                          'lambda',
                          params,
                          *top,
                          *body,
                          ),
                        ),
                      (
                        '',
                        ':',
                        ':*',
                        (
                          'itertools..starmap',
                          '_Qzwfz72h4o__lambda.__setattr__',
                          (
                            '.items',
                            (
                              'builtins..dict',
                              ':',
                              *doc,
                              'hissp.macros..__name__',
                              (
                                'quote',
                                name,
                                ),
                              'hissp.macros..__qualname__',
                              (
                                'quote',
                                qualname,
                                ),
                              'hissp.macros..__code__',
                              (
                                '.replace',
                                '_Qzwfz72h4o__lambda.__code__',
                                ':',
                                'hissp.macros..co_name',
                                (
                                  'quote',
                                  name,
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ':?',
                        '',
                        ),
                      '_Qzwfz72h4o__lambda',
                      )
                )(
                  *# ifQzH_else
                   (lambda b, c, a: c()if b else a())(
                     __import__('hissp').is_hissp_string(
                       maybeQzH_docstring),
                     (lambda :
                         (
                           (),
                           (
                             'hissp.macros.._macro_.__doc__',
                             maybeQzH_docstring,
                             ),
                           )
                     ),
                     (lambda :
                         (
                           (
                             maybeQzH_docstring,
                             ),
                           (),
                           )
                     )))
            )(
              *reversed(
                 qualname.split(
                   '.',
                   (1))))
        ):
   (__import__('builtins').setattr(
      _Qzew72czym__G,
      '__doc__',
      ('A lambda enhanced with a `qualified name` and optionally a docstring.\n'
       '\n'
       "  Hissp's (and Python's) lambda syntax do not have docstrings. Named\n"
       '  lambdas improve `REPL` transparency and error messages, at the cost of\n'
       '  some configuration overhead to set the name in the three places Python\n'
       '  requires.\n'
       '\n'
       '  Used by `defmacro` and `defun`. Not recommended for otherwise\n'
       '  anonymous functions due to the additional overhead.\n'
       '  ')),
    __import__('builtins').setattr(
      __import__('builtins').globals()['_macro_'],
      'fun',
      _Qzew72czym__G),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__code__',
      _Qzew72czym__G.__code__.replace(
        co_name='fun')),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__name__',
      'fun'),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'fun',))))  [-1]
)()

# defmacro
(
 lambda _Qzew72czym__G=(lambda condition, *body:
            (
              (
                'lambda',
                'ba',
                '()if b else a()',
                ),
              condition,
              (
                'lambda',
                ':',
                *body,
                ),
              )
        ):
   (__import__('builtins').setattr(
      _Qzew72czym__G,
      '__doc__',
      ('Unless the condition is true,\n'
       '  evaluates each expression in sequence for side effects,\n'
       '  resulting in the value of the last.\n'
       '  Otherwise, skips them and returns ``()``.\n'
       '\n'
       '  .. code-block:: REPL\n'
       '\n'
       "     #> (any-map c 'abcd\n"
       "     #..  (unless (op#eq c 'b)\n"
       '     #..    (print c)))\n'
       '     >>> # anyQzH_map\n'
       "     ... __import__('builtins').any(\n"
       "     ...   __import__('builtins').map(\n"
       '     ...     (lambda c:\n'
       '     ...         # unless\n'
       '     ...         (lambda b, a: ()if b else a())(\n'
       "     ...           __import__('operator').eq(\n"
       '     ...             c,\n'
       "     ...             'b'),\n"
       '     ...           (lambda :\n'
       '     ...               print(\n'
       '     ...                 c)\n'
       '     ...           ))\n'
       '     ...     ),\n'
       "     ...     'abcd'))\n"
       '     a\n'
       '     c\n'
       '     d\n'
       '     False\n'
       '\n'
       '  See also: `when`.\n'
       '  ')),
    __import__('builtins').setattr(
      __import__('builtins').globals()['_macro_'],
      'unless',
      _Qzew72czym__G),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__code__',
      _Qzew72czym__G.__code__.replace(
        co_name='unless')),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__name__',
      'unless'),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'unless',))))  [-1]
)()

# defmacro
(
 lambda _Qzew72czym__G=(lambda name, parameters, *body:
            # ifQzH_else
            (lambda b, c, a: c()if b else a())(
              name.startswith(
                ':'),
              (lambda :
                  exec(
                    "raise SyntaxError('name cannot be a control word (try a \\:)')")
              ),
              (lambda :
                  # let
                  (
                   lambda form=(
                            'builtins..setattr',
                            (
                              '.get',
                              (
                                'builtins..globals',
                                ),
                              "('_macro_')",
                              ),
                            (
                              'quote',
                              name,
                              ),
                            (
                              'hissp.macros.._macro_.fun',
                              ('_macro_.{}').format(
                                name),
                              parameters,
                              *body,
                              ),
                            ):
                      # ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('operator').contains(
                          __import__('hissp.compiler',fromlist='*').ENV.get(),
                          '_macro_'),
                        (lambda : form),
                        (lambda :
                            (
                              'hissp.macros.._macro_.progn',
                              (
                                '.setdefault',
                                (
                                  'builtins..globals',
                                  ),
                                "('_macro_')",
                                (
                                  'types..SimpleNamespace',
                                  ),
                                ),
                              form,
                              )
                        ))
                  )()
              ))
        ):
   (__import__('builtins').setattr(
      _Qzew72czym__G,
      '__doc__',
      ('Creates a new `macro function` for the current module.\n'
       '\n'
       "  If there's no local ``_macro_`` namespace (at compile time), adds code\n"
       "  to create one using `types.SimpleNamespace` (at runtime), if it's\n"
       "  still not there. If there's a docstring, stores it as the new lambda's\n"
       "  ``__doc__``. Adds the ``_macro_`` prefix to the lambda's\n"
       '  ``__qualname__``. Saves the lambda in ``_macro_`` using the given\n'
       '  attribute name.\n'
       '\n'
       '  .. code-block:: REPL\n'
       '\n'
       '     #> (defmacro p123 (sep)\n'
       '     #..  <#;Prints 1 2 3 with the given separator\n'
       '     #..  `(print 1 2 3 : sep ,sep))\n'
       '     >>> # defmacro\n'
       "     ... __import__('builtins').setattr(\n"
       "     ...   __import__('builtins').globals().get(\n"
       "     ...     ('_macro_')),\n"
       "     ...   'p123',\n"
       '     ...   # hissp.macros.._macro_.fun\n'
       '     ...   # hissp.macros.._macro_.let\n'
       '     ...   (\n'
       '     ...    lambda _Qzwin5lyqx__lambda=(lambda sep:\n'
       '     ...               (\n'
       "     ...                 'builtins..print',\n"
       '     ...                 (1),\n'
       '     ...                 (2),\n'
       '     ...                 (3),\n'
       "     ...                 ':',\n"
       "     ...                 '__main__..sep',\n"
       '     ...                 sep,\n'
       '     ...                 )\n'
       '     ...           ):\n'
       '     ...      ((\n'
       "     ...         *__import__('itertools').starmap(\n"
       '     ...            _Qzwin5lyqx__lambda.__setattr__,\n'
       "     ...            __import__('builtins').dict(\n"
       "     ...              __doc__='Prints 1 2 3 with the given separator',\n"
       "     ...              __name__='p123',\n"
       "     ...              __qualname__='_macro_.p123',\n"
       '     ...              __code__=_Qzwin5lyqx__lambda.__code__.replace(\n'
       "     ...                         co_name='p123')).items()),\n"
       '     ...         ),\n'
       '     ...       _Qzwin5lyqx__lambda)  [-1]\n'
       '     ...   )())\n'
       '\n'
       '     #> (p123 ::)\n'
       '     >>> # p123\n'
       "     ... __import__('builtins').print(\n"
       '     ...   (1),\n'
       '     ...   (2),\n'
       '     ...   (3),\n'
       "     ...   sep='::')\n"
       '     1::2::3\n'
       '\n'
       '  See also: `<# <QzLT_QzHASH_>`, `attach`, `lambda_`, `defun`.\n'
       '  ')),
    __import__('builtins').setattr(
      __import__('builtins').globals()['_macro_'],
      'defmacro',
      _Qzew72czym__G),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__code__',
      _Qzew72czym__G.__code__.replace(
        co_name='defmacro')),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__name__',
      'defmacro'),
    __import__('builtins').setattr(
      _Qzew72czym__G,
      '__qualname__',
      ('.').join(
        ('_macro_',
         'defmacro',))))  [-1]
)()

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'define',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda qualname, value:
              # ifQzH_else
              (lambda b, c, a: c()if b else a())(
                qualname.startswith(
                  ':'),
                (lambda :
                    exec(
                      "raise SyntaxError('qualname cannot be a control word (try a \\:)')")
                ),
                (lambda :
                    # letQzH_from
                    (lambda ns, _dot, attr:
                        # ifQzH_else
                        (lambda b, c, a: c()if b else a())(
                          ns,
                          (lambda :
                              (
                                'builtins..setattr',
                                ns,
                                (
                                  'quote',
                                  attr,
                                  ),
                                value,
                                )
                          ),
                          (lambda :
                              (
                                '.update',
                                (
                                  'builtins..globals',
                                  ),
                                ':',
                                qualname,
                                value,
                                )
                          ))
                    )(
                      *qualname.rpartition(
                         ('.')))
                ))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Assigns an attribute the value.\n'
                      '\n'
                      '  The qualname may be a `fully-qualified identifier` or start from a\n'
                      '  name in scope. Assigns an attribute of the current module (a global)\n'
                      "  if there's no `qualifier`.\n"
                      '\n'
                      '  .. code-block:: REPL\n'
                      '\n'
                      "     #> (define SPAM 'tomato)\n"
                      '     >>> # define\n'
                      "     ... __import__('builtins').globals().update(\n"
                      "     ...   SPAM='tomato')\n"
                      '\n'
                      '     #> SPAM\n'
                      '     >>> SPAM\n'
                      "     'tomato'\n"
                      '\n'
                      '  See also: `globals`, `dict.update`, `setattr`, `defonce`,\n'
                      '  `assignment`, `global`.\n'
                      '  '),
             __name__='define',
             __qualname__='_macro_.define',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='define')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'defun',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda qualname, params, *body:
              (
                'hissp.macros.._macro_.define',
                qualname,
                (
                  'hissp.macros.._macro_.fun',
                  qualname,
                  params,
                  *body,
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('`define` a `fun` with the same name.\n'
                      '\n'
                      '  See `deftypeonce` for how to define methods.\n'
                      '\n'
                      '  See also: `def`, `define`, `defmacro`, `:@## <QzCOLON_QzAT_QzHASH_>`.\n'
                      '  '),
             __name__='defun',
             __qualname__='_macro_.defun',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='defun')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'defonce',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda qualname, value:
              (
                'hissp.macros.._macro_.unless',
                # letQzH_from
                (lambda ns, _dot, attr:
                    # ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      ns,
                      (lambda :
                          (
                            'builtins..hasattr',
                            ns,
                            (
                              'quote',
                              attr,
                              ),
                            )
                      ),
                      (lambda :
                          (
                            'operator..contains',
                            (
                              'builtins..globals',
                              ),
                            (
                              'quote',
                              attr,
                              ),
                            )
                      ))
                )(
                  *qualname.rpartition(
                     ('.'))),
                (
                  'hissp.macros.._macro_.define',
                  qualname,
                  value,
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Defines an attribute, unless it exists.\n'
                      '\n'
                      "  Like `define`, but won't overwrite an existing attribute.\n"
                      '  Useful when sending the whole file to the `REPL` repeatedly or when\n'
                      '  using `importlib.reload`.\n'
                      '\n'
                      '  .. code-block:: REPL\n'
                      '\n'
                      '     #> (defonce CACHE (types..SimpleNamespace : x 1))\n'
                      '     >>> # defonce\n'
                      '     ... # hissp.macros.._macro_.unless\n'
                      '     ... (lambda b, a: ()if b else a())(\n'
                      "     ...   __import__('operator').contains(\n"
                      "     ...     __import__('builtins').globals(),\n"
                      "     ...     'CACHE'),\n"
                      '     ...   (lambda :\n'
                      '     ...       # hissp.macros.._macro_.define\n'
                      "     ...       __import__('builtins').globals().update(\n"
                      "     ...         CACHE=__import__('types').SimpleNamespace(\n"
                      '     ...                 x=(1)))\n'
                      '     ...   ))\n'
                      '\n'
                      "     #> (setattr CACHE 'x 42)\n"
                      '     >>> setattr(\n'
                      '     ...   CACHE,\n'
                      "     ...   'x',\n"
                      '     ...   (42))\n'
                      '\n'
                      "     #> (defonce CACHE (progn (print 'not 'evaluated)\n"
                      '     #..                      (types..SimpleNamespace : x 1)))\n'
                      '     >>> # defonce\n'
                      '     ... # hissp.macros.._macro_.unless\n'
                      '     ... (lambda b, a: ()if b else a())(\n'
                      "     ...   __import__('operator').contains(\n"
                      "     ...     __import__('builtins').globals(),\n"
                      "     ...     'CACHE'),\n"
                      '     ...   (lambda :\n'
                      '     ...       # hissp.macros.._macro_.define\n'
                      "     ...       __import__('builtins').globals().update(\n"
                      '     ...         CACHE=# progn\n'
                      '     ...               (print(\n'
                      "     ...                  'not',\n"
                      "     ...                  'evaluated'),\n"
                      "     ...                __import__('types').SimpleNamespace(\n"
                      '     ...                  x=(1)))  [-1])\n'
                      '     ...   ))\n'
                      '     ()\n'
                      '\n'
                      '     #> CACHE ; The second defonce had no effect.\n'
                      '     >>> CACHE\n'
                      '     namespace(x=42)\n'
                      '\n'
                      '  See also: `deftypeonce`, `hissp.refresh`.\n'
                      '\n'
                      '  '),
             __name__='defonce',
             __qualname__='_macro_.defonce',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='defonce')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'deftypeonce',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(
           lambda qualname,
                  bases=(),
                  *once_decorators:
              # let
              (
               lambda ibases=iter(
                        bases),
                      name=qualname.rpartition('.')[-1]:
                  (
                    'hissp.macros.._macro_.defonce',
                    qualname,
                    __import__('functools').reduce(
                      (lambda cls, f:
                          (
                            f,
                            cls,
                            )
                      ),
                      once_decorators,
                      (
                        'builtins..type',
                        (
                          'quote',
                          name,
                          ),
                        (
                          '',
                          *__import__('itertools').takewhile(
                             (lambda x:
                                 __import__('operator').ne(
                                   x,
                                   ':')
                             ),
                             ibases),
                          '',
                          ),
                        dict(),
                        ':',
                        *ibases,
                        )),
                    )
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Defines a `type` (`class`), unless it exists.\n'
                      '\n'
                      'Add class attributes afterward using `define` or `defun`, and class\n'
                      'decorators above with `:@## <QzCOLON_QzAT_QzHASH_>` or afterward\n'
                      'using `zap@ <zapQzAT_>`. These run again on module reload, updating\n'
                      'the existing class object, which can affect the behavior its\n'
                      'instances defined before the reload.\n'
                      '\n'
                      'The ``once_decorators`` apply before any external ones, in the\n'
                      'order written (first applies first), unless the type exists (not\n'
                      'reapplied on reloads). Beware that type attributes defined\n'
                      'afterward will not be available for the ``once_decorators`` to\n'
                      'operate upon. A decorator can add attributes for subsequent\n'
                      'decorators to operate upon, however, and a decorator may be a\n'
                      'lambda defined in line. It is possible to add arbitrary attributes\n'
                      "this way, but remember that ``once_decorators`` don't run again on\n"
                      'reloads, so changes here cannot simply be reloaded with the module\n'
                      'the way attributes defined afterward can.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (deftypeonce Point2D (tuple)\n'
                      '   #..  ;; Example of setting an attr with an internal decorator.\n'
                      '   #..  X#(attach X : __doc__ "Simple ordered pair."))\n'
                      '   >>> # deftypeonce\n'
                      '   ... # hissp.macros.._macro_.defonce\n'
                      '   ... # hissp.macros.._macro_.unless\n'
                      '   ... (lambda b, a: ()if b else a())(\n'
                      "   ...   __import__('operator').contains(\n"
                      "   ...     __import__('builtins').globals(),\n"
                      "   ...     'Point2D'),\n"
                      '   ...   (lambda :\n'
                      '   ...       # hissp.macros.._macro_.define\n'
                      "   ...       __import__('builtins').globals().update(\n"
                      '   ...         Point2D=(lambda X:\n'
                      '   ...                     # attach\n'
                      '   ...                     # hissp.macros.._macro_.let\n'
                      '   ...                     (lambda _Qzvibdgdly__target=X:\n'
                      "   ...                        (__import__('builtins').setattr(\n"
                      '   ...                           _Qzvibdgdly__target,\n'
                      "   ...                           '__doc__',\n"
                      "   ...                           ('Simple ordered pair.')),\n"
                      '   ...                         _Qzvibdgdly__target)  [-1]\n'
                      '   ...                     )()\n'
                      '   ...                 )(\n'
                      "   ...                   __import__('builtins').type(\n"
                      "   ...                     'Point2D',\n"
                      '   ...                     (\n'
                      '   ...                       tuple,\n'
                      '   ...                       ),\n'
                      '   ...                     {})))\n'
                      '   ...   ))\n'
                      '\n'
                      '   #> Point2D.__doc__\n'
                      '   >>> Point2D.__doc__\n'
                      "   'Simple ordered pair.'\n"
                      '\n'
                      '   #> (define Point2D.__doc__\n'
                      '   #..  "Attributes can also be defined afterwards.")\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').setattr(\n"
                      '   ...   Point2D,\n'
                      "   ...   '__doc__',\n"
                      "   ...   ('Attributes can also be defined afterwards.'))\n"
                      '\n'
                      '   #> Point2D.__doc__\n'
                      '   >>> Point2D.__doc__\n'
                      "   'Attributes can also be defined afterwards.'\n"
                      '\n'
                      '   #> (defun Point2D.__new__ (cls x y)\n'
                      '   #..  (.__new__ tuple cls `(,x ,y)))\n'
                      '   >>> # defun\n'
                      '   ... # hissp.macros.._macro_.define\n'
                      "   ... __import__('builtins').setattr(\n"
                      '   ...   Point2D,\n'
                      "   ...   '__new__',\n"
                      '   ...   # hissp.macros.._macro_.fun\n'
                      '   ...   # hissp.macros.._macro_.let\n'
                      '   ...   (\n'
                      '   ...    lambda _Qzzygff6yw__lambda=(lambda cls, x, y:\n'
                      '   ...               tuple.__new__(\n'
                      '   ...                 cls,\n'
                      '   ...                 (\n'
                      '   ...                   x,\n'
                      '   ...                   y,\n'
                      '   ...                   ))\n'
                      '   ...           ):\n'
                      '   ...      ((\n'
                      "   ...         *__import__('itertools').starmap(\n"
                      '   ...            _Qzzygff6yw__lambda.__setattr__,\n'
                      "   ...            __import__('builtins').dict(\n"
                      "   ...              __name__='__new__',\n"
                      "   ...              __qualname__='Point2D.__new__',\n"
                      '   ...              __code__=_Qzzygff6yw__lambda.__code__.replace(\n'
                      "   ...                         co_name='__new__')).items()),\n"
                      '   ...         ),\n'
                      '   ...       _Qzzygff6yw__lambda)  [-1]\n'
                      '   ...   )())\n'
                      '\n'
                      '   #> (defun Point2D.__repr__ (self)\n'
                      '   #..  (.format "Point2D({!r}, {!r})" : :* self))\n'
                      '   >>> # defun\n'
                      '   ... # hissp.macros.._macro_.define\n'
                      "   ... __import__('builtins').setattr(\n"
                      '   ...   Point2D,\n'
                      "   ...   '__repr__',\n"
                      '   ...   # hissp.macros.._macro_.fun\n'
                      '   ...   # hissp.macros.._macro_.let\n'
                      '   ...   (\n'
                      '   ...    lambda _Qzhdg2exzl__lambda=(lambda self:\n'
                      "   ...               ('Point2D({!r}, {!r})').format(\n"
                      '   ...                 *self)\n'
                      '   ...           ):\n'
                      '   ...      ((\n'
                      "   ...         *__import__('itertools').starmap(\n"
                      '   ...            _Qzhdg2exzl__lambda.__setattr__,\n'
                      "   ...            __import__('builtins').dict(\n"
                      "   ...              __name__='__repr__',\n"
                      "   ...              __qualname__='Point2D.__repr__',\n"
                      '   ...              __code__=_Qzhdg2exzl__lambda.__code__.replace(\n'
                      "   ...                         co_name='__repr__')).items()),\n"
                      '   ...         ),\n'
                      '   ...       _Qzhdg2exzl__lambda)  [-1]\n'
                      '   ...   )())\n'
                      '\n'
                      '   #> (Point2D 1 2)\n'
                      '   >>> Point2D(\n'
                      '   ...   (1),\n'
                      '   ...   (2))\n'
                      '   Point2D(1, 2)\n'
                      '\n'
                      'Also supports keyword arguments in the bases tuple for\n'
                      '`object.__init_subclass__`. Separate with a ``:``.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> :@##classmethod\n'
                      '   #..(defun Point2D.__init_subclass__ (cls :/ : :** kwargs)\n'
                      '   #..  "Just displays inputs"\n'
                      '   #..  (print kwargs))\n'
                      '   >>> # hissp.macros.._macro_.define\n'
                      "   ... __import__('builtins').setattr(\n"
                      '   ...   Point2D,\n'
                      "   ...   '__init_subclass__',\n"
                      '   ...   # hissp.macros.._macro_.progn\n'
                      '   ...   (# defun\n'
                      '   ...    # hissp.macros.._macro_.define\n'
                      "   ...    __import__('builtins').setattr(\n"
                      '   ...      Point2D,\n'
                      "   ...      '__init_subclass__',\n"
                      '   ...      # hissp.macros.._macro_.fun\n'
                      '   ...      # hissp.macros.._macro_.let\n'
                      '   ...      (\n'
                      '   ...       lambda _Qzujblvbnr__lambda=(lambda cls, /, **kwargs:\n'
                      '   ...                  print(\n'
                      '   ...                    kwargs)\n'
                      '   ...              ):\n'
                      '   ...         ((\n'
                      "   ...            *__import__('itertools').starmap(\n"
                      '   ...               _Qzujblvbnr__lambda.__setattr__,\n'
                      "   ...               __import__('builtins').dict(\n"
                      "   ...                 __doc__=('Just displays inputs'),\n"
                      "   ...                 __name__='__init_subclass__',\n"
                      "   ...                 __qualname__='Point2D.__init_subclass__',\n"
                      '   ...                 __code__=_Qzujblvbnr__lambda.__code__.replace(\n'
                      "   ...                            co_name='__init_subclass__')).items()),\n"
                      '   ...            ),\n'
                      '   ...          _Qzujblvbnr__lambda)  [-1]\n'
                      '   ...      )()),\n'
                      '   ...    classmethod(\n'
                      '   ...      Point2D.__init_subclass__))  [-1])\n'
                      '\n'
                      '   #> (deftypeonce ASubclass (Point2D : a 1  b 2))\n'
                      '   >>> # deftypeonce\n'
                      '   ... # hissp.macros.._macro_.defonce\n'
                      '   ... # hissp.macros.._macro_.unless\n'
                      '   ... (lambda b, a: ()if b else a())(\n'
                      "   ...   __import__('operator').contains(\n"
                      "   ...     __import__('builtins').globals(),\n"
                      "   ...     'ASubclass'),\n"
                      '   ...   (lambda :\n'
                      '   ...       # hissp.macros.._macro_.define\n'
                      "   ...       __import__('builtins').globals().update(\n"
                      "   ...         ASubclass=__import__('builtins').type(\n"
                      "   ...                     'ASubclass',\n"
                      '   ...                     (\n'
                      '   ...                       Point2D,\n'
                      '   ...                       ),\n'
                      '   ...                     {},\n'
                      '   ...                     a=(1),\n'
                      '   ...                     b=(2)))\n'
                      '   ...   ))\n'
                      "   {'a': 1, 'b': 2}\n"
                      '\n'
                      'See also: `attach`, `types.new_class`, `defonce`.\n'),
             __name__='deftypeonce',
             __qualname__='_macro_.deftypeonce',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='deftypeonce')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'deftupleonce',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda typename, *args:
              (
                'hissp.macros.._macro_.defonce',
                typename,
                (
                  'collections..namedtuple',
                  (
                    'quote',
                    typename,
                    ),
                  *args,
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Defines a `collections.namedtuple` unless it exists.\n'
                      '\n'
                      '  .. code-block:: REPL\n'
                      '\n'
                      "     #> (deftupleonce Vec3D '(x y z) : defaults '(0 0 0))\n"
                      '     >>> # deftupleonce\n'
                      '     ... # hissp.macros.._macro_.defonce\n'
                      '     ... # hissp.macros.._macro_.unless\n'
                      '     ... (lambda b, a: ()if b else a())(\n'
                      "     ...   __import__('operator').contains(\n"
                      "     ...     __import__('builtins').globals(),\n"
                      "     ...     'Vec3D'),\n"
                      '     ...   (lambda :\n'
                      '     ...       # hissp.macros.._macro_.define\n'
                      "     ...       __import__('builtins').globals().update(\n"
                      "     ...         Vec3D=__import__('collections').namedtuple(\n"
                      "     ...                 'Vec3D',\n"
                      "     ...                 ('x',\n"
                      "     ...                  'y',\n"
                      "     ...                  'z',),\n"
                      '     ...                 defaults=((0),\n'
                      '     ...                           (0),\n'
                      '     ...                           (0),)))\n'
                      '     ...   ))\n'
                      '\n'
                      '  Like `deftypeonce`, methods can be attached afterward. On reload, the\n'
                      '  existing class is modified, affecting all of its instances, including\n'
                      '  those created before the reload.\n'
                      '\n'
                      '  .. code-block:: REPL\n'
                      '\n'
                      '     #> (define offset (Vec3D : z 1  x 2))\n'
                      '     >>> # define\n'
                      "     ... __import__('builtins').globals().update(\n"
                      '     ...   offset=Vec3D(\n'
                      '     ...            z=(1),\n'
                      '     ...            x=(2)))\n'
                      '\n'
                      '     #> (defun Vec3D.__add__ (self other)\n'
                      '     #..  (._make Vec3D (map op#add self other)))\n'
                      '     >>> # defun\n'
                      '     ... # hissp.macros.._macro_.define\n'
                      "     ... __import__('builtins').setattr(\n"
                      '     ...   Vec3D,\n'
                      "     ...   '__add__',\n"
                      '     ...   # hissp.macros.._macro_.fun\n'
                      '     ...   # hissp.macros.._macro_.let\n'
                      '     ...   (\n'
                      '     ...    lambda _Qzz7drxadm__lambda=(lambda self, other:\n'
                      '     ...               Vec3D._make(\n'
                      '     ...                 map(\n'
                      "     ...                   __import__('operator').add,\n"
                      '     ...                   self,\n'
                      '     ...                   other))\n'
                      '     ...           ):\n'
                      '     ...      ((\n'
                      "     ...         *__import__('itertools').starmap(\n"
                      '     ...            _Qzz7drxadm__lambda.__setattr__,\n'
                      "     ...            __import__('builtins').dict(\n"
                      "     ...              __name__='__add__',\n"
                      "     ...              __qualname__='Vec3D.__add__',\n"
                      '     ...              __code__=_Qzz7drxadm__lambda.__code__.replace(\n'
                      "     ...                         co_name='__add__')).items()),\n"
                      '     ...         ),\n'
                      '     ...       _Qzz7drxadm__lambda)  [-1]\n'
                      '     ...   )())\n'
                      '\n'
                      '     #> (op#add offset offset)\n'
                      "     >>> __import__('operator').add(\n"
                      '     ...   offset,\n'
                      '     ...   offset)\n'
                      '     Vec3D(x=4, y=0, z=2)\n'
                      '\n'
                      '     #> (op#add _ (Vec3D 10 20 30))\n'
                      "     >>> __import__('operator').add(\n"
                      '     ...   _,\n'
                      '     ...   Vec3D(\n'
                      '     ...     (10),\n'
                      '     ...     (20),\n'
                      '     ...     (30)))\n'
                      '     Vec3D(x=14, y=20, z=32)\n'
                      '\n'
                      '  '),
             __name__='deftupleonce',
             __qualname__='_macro_.deftupleonce',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='deftupleonce')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzCOLON_QzAT_QzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda decoration, definition:
              # let
              (
               lambda qualname=definition.__getitem__(
                        (1)):
                  (
                    'hissp.macros.._macro_.define',
                    qualname,
                    (
                      'hissp.macros.._macro_.progn',
                      definition,
                      (
                        decoration,
                        qualname,
                        ),
                      ),
                    )
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``:@##`` 'decorator' applies ``decoration`` to definition & reassigns.\n"
                      '\n'
                      '  ``definition`` form must assign an attribute identified by its first\n'
                      '  arg. Expands to a `define`, meaning decorators can stack.\n'
                      '\n'
                      '  Decorator syntax is for definitions, like `define` and `defun`, and\n'
                      '  would work on any definition macro that has the definition qualname as\n'
                      '  its first argument (not `defmacro`, but `defun` can target the\n'
                      '  ``_macro_`` namespace if it exists).\n'
                      '\n'
                      '  Use `zap@ <zapQzAT_>` to decorate an attribute after its definition.\n'
                      '\n'
                      '  .. code-block:: REPL\n'
                      '\n'
                      '     #> :@##.swapcase\n'
                      '     #..:@##.title\n'
                      "     #..(define spam 'spam) ; Unlike Python def, not always a function.\n"
                      '     >>> # hissp.macros.._macro_.define\n'
                      "     ... __import__('builtins').globals().update(\n"
                      '     ...   spam=# hissp.macros.._macro_.progn\n'
                      '     ...        (# hissp.macros.._macro_.define\n'
                      "     ...         __import__('builtins').globals().update(\n"
                      '     ...           spam=# hissp.macros.._macro_.progn\n'
                      '     ...                (# define\n'
                      "     ...                 __import__('builtins').globals().update(\n"
                      "     ...                   spam='spam'),\n"
                      '     ...                 spam.title())  [-1]),\n'
                      '     ...         spam.swapcase())  [-1])\n'
                      '\n'
                      '     #> spam\n'
                      '     >>> spam\n'
                      "     'sPAM'\n"
                      '\n'
                      '  '),
             __name__='QzCOLON_QzAT_QzHASH_',
             __qualname__='_macro_.QzCOLON_QzAT_QzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzCOLON_QzAT_QzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzLT_QzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda comment:
              (
                'quote',
                comment.contents(),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``<#`` 'comment string' tag.\n"
                      '\n'
                      'Converts a block of line comments to a raw string.\n'
                      "Roughly equivalent to ``'hissp.reader..Comment.contents#``.\n"
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> <#;You won't have to\n"
                      '   #..;; escape the "quotes".\n'
                      '   #..\n'
                      '   >>> \'You won\\\'t have to\\nescape the "quotes".\'\n'
                      '   \'You won\\\'t have to\\nescape the "quotes".\'\n'
                      '\n'
                      'See also: `triple-quoted string`, `hissp.reader.Comment`.\n'),
             __name__='QzLT_QzHASH_',
             __qualname__='_macro_.QzLT_QzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzLT_QzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'OQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr:
              (
                'lambda',
                ':',
                expr,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``O#`` 'thunk' Make ``expr`` an anonymous function body with no parameters.\n"
                      '\n'
                      'See also: `X# <XQzHASH_>`.\n'),
             __name__='OQzHASH_',
             __qualname__='_macro_.OQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='OQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'XQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr:
              (
                'lambda',
                'X',
                expr,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``X#`` Anaphoric. Make ``expr`` an anonymous function with parameter X.\n'
                      '\n'
                      'Examples:\n'
                      '\n'
                      'Convert macro to function.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (list (map X#(@ X) "abc")) ; en#list would also work here.\n'
                      '   >>> list(\n'
                      '   ...   map(\n'
                      '   ...     (lambda X:\n'
                      '   ...         # QzAT_\n'
                      '   ...         (lambda *xs: [*xs])(\n'
                      '   ...           X)\n'
                      '   ...     ),\n'
                      "   ...     ('abc')))\n"
                      "   [['a'], ['b'], ['c']]\n"
                      '\n'
                      'Compact function definition using Python operators.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (define teen? X#|13<=X<20|)\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   teenQzQUERY_=(lambda X: 13<=X<20))\n'
                      '\n'
                      '   #> (teen? 12.5)\n'
                      '   >>> teenQzQUERY_(\n'
                      '   ...   (12.5))\n'
                      '   False\n'
                      '\n'
                      '   #> (teen? 19.5)\n'
                      '   >>> teenQzQUERY_(\n'
                      '   ...   (19.5))\n'
                      '   True\n'
                      '\n'
                      'Get an attribute without calling it.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (X#X.upper "shout")\n'
                      '   >>> (lambda X: X.upper)(\n'
                      "   ...   ('shout'))\n"
                      '   <built-in method upper of str object at ...>\n'
                      '\n'
                      '   #> (_)\n'
                      '   >>> _()\n'
                      "   'SHOUT'\n"
                      '\n'
                      '   #> (define class-name X#X.__class__.__name__) ; Attributes chain.\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   classQzH_name=(lambda X: X.__class__.__name__))\n'
                      '\n'
                      '   #> (class-name object)\n'
                      '   >>> classQzH_name(\n'
                      '   ...   object)\n'
                      "   'type'\n"
                      '\n'
                      '   #> (class-name "foo")\n'
                      '   >>> classQzH_name(\n'
                      "   ...   ('foo'))\n"
                      "   'str'\n"
                      '\n'
                      'See also:\n'
                      '`en# <enQzHASH_>`, `O# <OQzHASH_>`, `XY# <XYQzHASH_>`,\n'
                      '`@# <QzAT_QzHASH_>`, `operator.attrgetter`, `lambda`.\n'),
             __name__='XQzHASH_',
             __qualname__='_macro_.XQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='XQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'XYQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr:
              (
                'lambda',
                'XY',
                expr,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``XY#`` Anaphoric. Make ``expr`` an anonymous function with parameters X Y.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (functools..reduce XY#(op#concat Y X) 'abcd)\n"
                      "   >>> __import__('functools').reduce(\n"
                      '   ...   (lambda X, Y:\n'
                      "   ...       __import__('operator').concat(\n"
                      '   ...         Y,\n'
                      '   ...         X)\n'
                      '   ...   ),\n'
                      "   ...   'abcd')\n"
                      "   'dcba'\n"
                      '\n'
                      'See also:\n'
                      '`X# <XQzHASH_>`, `/XY# <QzSOL_XYQzHASH_>`, `XYZ# <XYZQzHASH_>`.\n'),
             __name__='XYQzHASH_',
             __qualname__='_macro_.XYQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='XYQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'XYZQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr:
              (
                'lambda',
                'XYZ',
                expr,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``XYZ#`` Anaphoric. Make ``expr`` an anonymous function with parameters X Y '
                      'Z.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (XYZ#|X*Y == Z| : X math..pi  Y 2  Z math..tau)\n'
                      '   >>> (lambda X, Y, Z: X*Y == Z)(\n'
                      "   ...   X=__import__('math').pi,\n"
                      '   ...   Y=(2),\n'
                      "   ...   Z=__import__('math').tau)\n"
                      '   True\n'
                      '\n'
                      'See also: `XY# <XYQzHASH_>`, `XYZW# <XYZWQzHASH_>`.\n'),
             __name__='XYZQzHASH_',
             __qualname__='_macro_.XYZQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='XYZQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'XYZWQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr:
              (
                'lambda',
                'XYZW',
                expr,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``XYZW#`` Anaphoric. Make ``expr`` an anonymous function with parameters X Y '
                      'Z W.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (XYZW#|X[Y:Z:W]| "QuaoblcldefHg" -2 1 -2)\n'
                      '   >>> (lambda X, Y, Z, W: X[Y:Z:W])(\n'
                      "   ...   ('QuaoblcldefHg'),\n"
                      '   ...   (-2),\n'
                      '   ...   (1),\n'
                      '   ...   (-2))\n'
                      "   'Hello'\n"
                      '\n'
                      'See also: `XYZ# <XYZQzHASH_>`, `en# <enQzHASH_>`, `X# <XQzHASH_>`.\n'),
             __name__='XYZWQzHASH_',
             __qualname__='_macro_.XYZWQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='XYZWQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzSOL_XYQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr:
              (
                'functools..partial',
                'functools..reduce',
                (
                  'lambda',
                  'XY',
                  expr,
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``/XY#`` 'reduce X Y' Anaphoric.\n"
                      '\n'
                      'Make ``expr`` a reducing function with parameters X Y.\n'
                      'The resulting function is a partial application of\n'
                      '`functools.reduce`.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> /XY#(op#add Y X)\n'
                      "   >>> __import__('functools').partial(\n"
                      "   ...   __import__('functools').reduce,\n"
                      '   ...   (lambda X, Y:\n'
                      "   ...       __import__('operator').add(\n"
                      '   ...         Y,\n'
                      '   ...         X)\n'
                      '   ...   ))\n'
                      '   functools.partial(<built-in function reduce>, <function <lambda> at '
                      '0x...>)\n'
                      '\n'
                      "   #> (_ 'ABCD)\n"
                      '   >>> _(\n'
                      "   ...   'ABCD')\n"
                      "   'DCBA'\n"
                      '\n'
                      'See also: `XY# <XYQzHASH_>`, `/# <QzSOL_QzHASH_>`.\n'),
             __name__='QzSOL_XYQzHASH_',
             __qualname__='_macro_.QzSOL_XYQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzSOL_XYQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'alias',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda abbreviation, qualifier:
              (
                'hissp.macros.._macro_.defmacro',
                ('{}{}').format(
                  abbreviation.replace(
                    '.',
                    'QzDOT_'),
                  'QzHASH_'),
                (
                  '_Qzqqk7vl3n__attr',
                  ':/',
                  ':',
                  ':*',
                  '_Qzqqk7vl3n__args',
                  ':**',
                  '_Qzqqk7vl3n__kwargs',
                  ),
                (
                  'quote',
                  ('Aliases ``{}`` as ``{}#``.').format(
                    qualifier,
                    abbreviation),
                  ),
                (
                  'hissp.macros.._macro_.let',
                  (
                    '_Qzqqk7vl3n__attr',
                    (
                      'hissp.macros.._macro_.ifQzH_else',
                      (
                        'hissp..is_control',
                        '_Qzqqk7vl3n__attr',
                        ),
                      (
                        '.format',
                        "('_macro_.{}{}')",
                        (
                          'hissp..munge',
                          (
                            '.removeprefix',
                            '_Qzqqk7vl3n__attr',
                            (
                              'quote',
                              ':',
                              ),
                            ),
                          ),
                        (
                          'hissp.macros.._macro_.ifQzH_else',
                          (
                            'hissp.macros.._macro_.ifQzH_else',
                            '_Qzqqk7vl3n__args',
                            ':or',
                            '_Qzqqk7vl3n__kwargs',
                            ),
                          (
                            'quote',
                            'QzHASH_',
                            ),
                          "('')",
                          ),
                        ),
                      '_Qzqqk7vl3n__attr',
                      ),
                    ),
                  (
                    'hissp.macros.._macro_.ifQzH_else',
                    (
                      'hissp.macros.._macro_.ifQzH_else',
                      '_Qzqqk7vl3n__args',
                      ':or',
                      '_Qzqqk7vl3n__kwargs',
                      ),
                    (
                      (
                        (
                          'operator..attrgetter',
                          '_Qzqqk7vl3n__attr',
                          ),
                        qualifier,
                        ),
                      ':',
                      ':*',
                      '_Qzqqk7vl3n__args',
                      ':**',
                      '_Qzqqk7vl3n__kwargs',
                      ),
                    (
                      '.format',
                      "('{}.{}')",
                      (
                        'quote',
                        qualifier,
                        ),
                      '_Qzqqk7vl3n__attr',
                      ),
                    ),
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Defines a `tag` abbreviation of a `qualifier`.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (hissp.._macro_.alias H hissp.)\n'
                      '   >>> # hissp.._macro_.alias\n'
                      '   ... # hissp.macros.._macro_.defmacro\n'
                      "   ... __import__('builtins').setattr(\n"
                      "   ...   __import__('builtins').globals().get(\n"
                      "   ...     ('_macro_')),\n"
                      "   ...   'HQzHASH_',\n"
                      '   ...   # hissp.macros.._macro_.fun\n'
                      '   ...   # hissp.macros.._macro_.let\n'
                      '   ...   (\n'
                      '   ...    lambda _Qzwxh432ki__lambda=(lambda _Qzrtjqfxk2__attr, /, '
                      '*_Qzrtjqfxk2__args, **_Qzrtjqfxk2__kwargs:\n'
                      '   ...               # hissp.macros.._macro_.let\n'
                      '   ...               (\n'
                      '   ...                lambda _Qzrtjqfxk2__attr=# '
                      'hissp.macros.._macro_.ifQzH_else\n'
                      '   ...                       (lambda b, c, a: c()if b else a())(\n'
                      "   ...                         __import__('hissp').is_control(\n"
                      '   ...                           _Qzrtjqfxk2__attr),\n'
                      '   ...                         (lambda :\n'
                      "   ...                             ('_macro_.{}{}').format(\n"
                      "   ...                               __import__('hissp').munge(\n"
                      '   ...                                 _Qzrtjqfxk2__attr.removeprefix(\n'
                      "   ...                                   ':')),\n"
                      '   ...                               # hissp.macros.._macro_.ifQzH_else\n'
                      '   ...                               (lambda b, c, a: c()if b else a())(\n'
                      '   ...                                 # hissp.macros.._macro_.ifQzH_else\n'
                      '   ...                                 (lambda b, c, a: c()if b else a())(\n'
                      '   ...                                   _Qzrtjqfxk2__args,\n'
                      "   ...                                   (lambda : ':or'),\n"
                      '   ...                                   (lambda : _Qzrtjqfxk2__kwargs)),\n'
                      "   ...                                 (lambda : 'QzHASH_'),\n"
                      "   ...                                 (lambda : (''))))\n"
                      '   ...                         ),\n'
                      '   ...                         (lambda : _Qzrtjqfxk2__attr)):\n'
                      '   ...                   # hissp.macros.._macro_.ifQzH_else\n'
                      '   ...                   (lambda b, c, a: c()if b else a())(\n'
                      '   ...                     # hissp.macros.._macro_.ifQzH_else\n'
                      '   ...                     (lambda b, c, a: c()if b else a())(\n'
                      '   ...                       _Qzrtjqfxk2__args,\n'
                      "   ...                       (lambda : ':or'),\n"
                      '   ...                       (lambda : _Qzrtjqfxk2__kwargs)),\n'
                      '   ...                     (lambda :\n'
                      "   ...                         __import__('operator').attrgetter(\n"
                      '   ...                           _Qzrtjqfxk2__attr)(\n'
                      "   ...                           __import__('hissp'))(\n"
                      '   ...                           *_Qzrtjqfxk2__args,\n'
                      '   ...                           **_Qzrtjqfxk2__kwargs)\n'
                      '   ...                     ),\n'
                      '   ...                     (lambda :\n'
                      "   ...                         ('{}.{}').format(\n"
                      "   ...                           'hissp.',\n"
                      '   ...                           _Qzrtjqfxk2__attr)\n'
                      '   ...                     ))\n'
                      '   ...               )()\n'
                      '   ...           ):\n'
                      '   ...      ((\n'
                      "   ...         *__import__('itertools').starmap(\n"
                      '   ...            _Qzwxh432ki__lambda.__setattr__,\n'
                      "   ...            __import__('builtins').dict(\n"
                      "   ...              __doc__='Aliases ``hissp.`` as ``H#``.',\n"
                      "   ...              __name__='HQzHASH_',\n"
                      "   ...              __qualname__='_macro_.HQzHASH_',\n"
                      '   ...              __code__=_Qzwxh432ki__lambda.__code__.replace(\n'
                      "   ...                         co_name='HQzHASH_')).items()),\n"
                      '   ...         ),\n'
                      '   ...       _Qzwxh432ki__lambda)  [-1]\n'
                      '   ...   )())\n'
                      '\n'
                      "   #> 'H#munge ; New tag prepends qualifier.\n"
                      "   >>> 'hissp..munge'\n"
                      "   'hissp..munge'\n"
                      '\n'
                      '   #> (H#munge "*") ; Normal function call.\n'
                      "   >>> __import__('hissp').munge(\n"
                      "   ...   ('*'))\n"
                      "   'QzSTAR_'\n"
                      '\n'
                      "   #> 'H##munge|*| ; Read-time apply, like a fully-qualified tag.\n"
                      "   >>> 'QzSTAR_'\n"
                      "   'QzSTAR_'\n"
                      '\n'
                      "   #> 'H#:let-from ; control word inserts _macro_. Still munges.\n"
                      "   >>> 'hissp.._macro_.letQzH_from'\n"
                      "   'hissp.._macro_.letQzH_from'\n"
                      '\n'
                      '   #> (H#:let-from ab "AB" b) ; Macro form.\n'
                      '   >>> # hissp.._macro_.letQzH_from\n'
                      '   ... (lambda a, b: b)(\n'
                      "   ...   *('AB'))\n"
                      "   'B'\n"
                      '\n'
                      "   #> H#|:b#| ;b# tag's callable. Note #.\n"
                      "   >>> __import__('hissp')._macro_.bQzHASH_\n"
                      '   <function _macro_.bQzHASH_ at ...>\n'
                      '\n'
                      '   #> (H#:b\\#"b# at compile time") ; Macro form. :b\\# == |:b#|\n'
                      '   >>> # hissp.._macro_.bQzHASH_\n'
                      "   ... b'b# at compile time'\n"
                      "   b'b# at compile time'\n"
                      '\n'
                      '   #> hissp.._macro_.b#"Fully-qualified b# at read time." ; \\# implied.\n'
                      "   >>> b'Fully-qualified b# at read time.'\n"
                      "   b'Fully-qualified b# at read time.'\n"
                      '\n'
                      '   #> H##:b"Read-time b# via alias." ; \\# implied.\n'
                      "   >>> b'Read-time b# via alias.'\n"
                      "   b'Read-time b# via alias.'\n"
                      '\n'
                      "   #> H###:@ ns=math. name='tau ; Kwargs also work.\n"
                      "   >>> __import__('operator').attrgetter(\n"
                      "   ...   'tau')(\n"
                      "   ...   __import__('math'))\n"
                      '   6.283185307179586\n'
                      '\n'
                      'The bundled `op# <opQzHASH_>` and `i# <iQzHASH_>` tags are aliases\n'
                      'for `operator` and `itertools`, respectively.\n'
                      '\n'
                      'See also: `prelude`, `attach`, `hissp.alias`.\n'
                      '\n'),
             __name__='alias',
             __qualname__='_macro_.alias',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='alias')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'colQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('collections'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'collections.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``collections.`` as ``col#``.',
             __name__='colQzHASH_',
             __qualname__='_macro_.colQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='colQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'dtQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('datetime'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'datetime.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``datetime.`` as ``dt#``.',
             __name__='dtQzHASH_',
             __qualname__='_macro_.dtQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='dtQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'ftQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('functools'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'functools.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``functools.`` as ``ft#``.',
             __name__='ftQzHASH_',
             __qualname__='_macro_.ftQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='ftQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'hshQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('hashlib'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'hashlib.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``hashlib.`` as ``hsh#``.',
             __name__='hshQzHASH_',
             __qualname__='_macro_.hshQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='hshQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'iQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('itertools'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'itertools.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``itertools.`` as ``i#``.',
             __name__='iQzHASH_',
             __qualname__='_macro_.iQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='iQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'mpQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('multiprocessing'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'multiprocessing.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``multiprocessing.`` as ``mp#``.',
             __name__='mpQzHASH_',
             __qualname__='_macro_.mpQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='mpQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'mpQzDOT_smQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('multiprocessing.shared_memory',fromlist='*'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'multiprocessing.shared_memory.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``multiprocessing.shared_memory.`` as ``mp.sm#``.',
             __name__='mpQzDOT_smQzHASH_',
             __qualname__='_macro_.mpQzDOT_smQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='mpQzDOT_smQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'opQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('operator'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'operator.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``operator.`` as ``op#``.',
             __name__='opQzHASH_',
             __qualname__='_macro_.opQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='opQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'spQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('subprocess'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'subprocess.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``subprocess.`` as ``sp#``.',
             __name__='spQzHASH_',
             __qualname__='_macro_.spQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='spQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'tfQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('tempfile'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'tempfile.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``tempfile.`` as ``tf#``.',
             __name__='tfQzHASH_',
             __qualname__='_macro_.tfQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='tfQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'thrQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('threading'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'threading.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``threading.`` as ``thr#``.',
             __name__='thrQzHASH_',
             __qualname__='_macro_.thrQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='thrQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'tbQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('traceback'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'traceback.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``traceback.`` as ``tb#``.',
             __name__='tbQzHASH_',
             __qualname__='_macro_.tbQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='tbQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'utQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('unittest'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'unittest.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``unittest.`` as ``ut#``.',
             __name__='utQzHASH_',
             __qualname__='_macro_.utQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='utQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'mkQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('unittest.mock',fromlist='*'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'unittest.mock.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``unittest.mock.`` as ``mk#``.',
             __name__='mkQzHASH_',
             __qualname__='_macro_.mkQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='mkQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'wrnQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('warnings'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'warnings.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``warnings.`` as ``wrn#``.',
             __name__='wrnQzHASH_',
             __qualname__='_macro_.wrnQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='wrnQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'bnQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('builtins'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'builtins.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``builtins.`` as ``bn#``.',
             __name__='bnQzHASH_',
             __qualname__='_macro_.bnQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='bnQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'cxvQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('contextvars'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'contextvars.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``contextvars.`` as ``cxv#``.',
             __name__='cxvQzHASH_',
             __qualname__='_macro_.cxvQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='cxvQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'fiQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('fileinput'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'fileinput.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``fileinput.`` as ``fi#``.',
             __name__='fiQzHASH_',
             __qualname__='_macro_.fiQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='fiQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'impQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('importlib'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'importlib.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``importlib.`` as ``imp#``.',
             __name__='impQzHASH_',
             __qualname__='_macro_.impQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='impQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'impQzDOT_rQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('importlib.resources',fromlist='*'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'importlib.resources.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``importlib.resources.`` as ``imp.r#``.',
             __name__='impQzDOT_rQzHASH_',
             __qualname__='_macro_.impQzDOT_rQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='impQzDOT_rQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'nspQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('inspect'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'inspect.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``inspect.`` as ``nsp#``.',
             __name__='nspQzHASH_',
             __qualname__='_macro_.nspQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='nspQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'plQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('pathlib'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'pathlib.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``pathlib.`` as ``pl#``.',
             __name__='plQzHASH_',
             __qualname__='_macro_.plQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='plQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'twQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('textwrap'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'textwrap.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``textwrap.`` as ``tw#``.',
             __name__='twQzHASH_',
             __qualname__='_macro_.twQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='twQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# alias
# hissp.macros.._macro_.defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'HQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda _Qzqqk7vl3n__attr, /, *_Qzqqk7vl3n__args, **_Qzqqk7vl3n__kwargs:
              # hissp.macros.._macro_.let
              (
               lambda _Qzqqk7vl3n__attr=# hissp.macros.._macro_.ifQzH_else
                      (lambda b, c, a: c()if b else a())(
                        __import__('hissp').is_control(
                          _Qzqqk7vl3n__attr),
                        (lambda :
                            ('_macro_.{}{}').format(
                              __import__('hissp').munge(
                                _Qzqqk7vl3n__attr.removeprefix(
                                  ':')),
                              # hissp.macros.._macro_.ifQzH_else
                              (lambda b, c, a: c()if b else a())(
                                # hissp.macros.._macro_.ifQzH_else
                                (lambda b, c, a: c()if b else a())(
                                  _Qzqqk7vl3n__args,
                                  (lambda : ':or'),
                                  (lambda : _Qzqqk7vl3n__kwargs)),
                                (lambda : 'QzHASH_'),
                                (lambda : (''))))
                        ),
                        (lambda : _Qzqqk7vl3n__attr)):
                  # hissp.macros.._macro_.ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    # hissp.macros.._macro_.ifQzH_else
                    (lambda b, c, a: c()if b else a())(
                      _Qzqqk7vl3n__args,
                      (lambda : ':or'),
                      (lambda : _Qzqqk7vl3n__kwargs)),
                    (lambda :
                        __import__('operator').attrgetter(
                          _Qzqqk7vl3n__attr)(
                          __import__('hissp'))(
                          *_Qzqqk7vl3n__args,
                          **_Qzqqk7vl3n__kwargs)
                    ),
                    (lambda :
                        ('{}.{}').format(
                          'hissp.',
                          _Qzqqk7vl3n__attr)
                    ))
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__='Aliases ``hissp.`` as ``H#``.',
             __name__='HQzHASH_',
             __qualname__='_macro_.HQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='HQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'chainQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda xss:
              (
                'itertools..chain.from_iterable',
                xss,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``chain#`` Abbreviation for `itertools.chain.from_iterable`.'),
             __name__='chainQzHASH_',
             __qualname__='_macro_.chainQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='chainQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzET_QzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda callableQzPLUS_args:
              (
                'functools..partial',
                *callableQzPLUS_args,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``&#`` Abbreviation for `functools.partial`.'),
             __name__='QzET_QzHASH_',
             __qualname__='_macro_.QzET_QzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzET_QzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzBANG_QzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(
           lambda key,
                  items=(''):
              (
                (
                  'operator..itemgetter',
                  key,
                  ),
                items,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``!#`` 'look up in' Gets an item from items.\n"
                      '\n'
                      'Mnemonic: !tem.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (define first &#!#0)                    ;Gets an item by index.\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      "   ...   first=__import__('functools').partial(\n"
                      "   ...           __import__('operator').itemgetter(\n"
                      '   ...             (0)),\n'
                      '   ...           ))\n'
                      '\n'
                      '   #> (first "abc")\n'
                      '   >>> first(\n'
                      "   ...   ('abc'))\n"
                      "   'a'\n"
                      '\n'
                      '   #> !##(slice None None -1) "abc"           ;Slicing without injection.\n'
                      "   >>> __import__('operator').itemgetter(\n"
                      '   ...   slice(\n'
                      '   ...     None,\n'
                      '   ...     None,\n'
                      '   ...     (-1)))(\n'
                      "   ...   ('abc'))\n"
                      "   'cba'\n"
                      '\n'
                      "   #> !##'+ (dict : foo 2  + 1)               ;These also work on dicts.\n"
                      "   >>> __import__('operator').itemgetter(\n"
                      "   ...   'QzPLUS_')(\n"
                      '   ...   dict(\n'
                      '   ...     foo=(2),\n'
                      '   ...     QzPLUS_=(1)))\n'
                      '   1\n'
                      '\n'
                      "   #> (-> '(foo bar) !#1 .upper !#1)          ;Unary compatible with ->.\n"
                      '   >>> # QzH_QzGT_\n'
                      "   ... __import__('operator').itemgetter(\n"
                      '   ...   (1))(\n'
                      "   ...   __import__('operator').itemgetter(\n"
                      '   ...     (1))(\n'
                      "   ...     ('foo',\n"
                      "   ...      'bar',),\n"
                      '   ...     ).upper(),\n'
                      '   ...   )\n'
                      "   'A'\n"
                      '\n'
                      'See also: `operator.getitem`, `operator.itemgetter`,\n'
                      '`[# <QzLSQB_QzHASH_>`, `set! <setQzBANG_>`, `&# <QzET_QzHASH_>`,\n'
                      '`@# <QzAT_QzHASH_>`.\n'),
             __name__='QzBANG_QzHASH_',
             __qualname__='_macro_.QzBANG_QzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzBANG_QzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzLSQB_QzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(
           lambda lookup,
                  items=(''):
              (
                (
                  'lambda',
                  (
                    '_Qzud7xb74e__items',
                    ),
                  ('({}[{})').format(
                    '_Qzud7xb74e__items',
                    __import__('hissp').demunge(
                      lookup)),
                  ),
                items,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``[#`` 'subscript' Injection. Python's subscription operator.\n"
                      '\n'
                      'Interpret the lookup as Python code prepended with a ``[``.\n'
                      "Primarily used for Python's slice notation, but unrestricted.\n"
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> [##1][::2] '(foo bar)\n"
                      '   >>> (lambda _Qznxnvf5z5__items: (_Qznxnvf5z5__items[1][::2]))(\n'
                      "   ...   ('foo',\n"
                      "   ...    'bar',))\n"
                      "   'br'\n"
                      '\n'
                      'Unary compatible with `-> <QzH_QzGT_>` and `&# <QzET_QzHASH_>`.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (-> '(foo bar) [#1] .upper [#::2])\n"
                      '   >>> # QzH_QzGT_\n'
                      '   ... (lambda _Qznxnvf5z5__items: (_Qznxnvf5z5__items[::2]))(\n'
                      '   ...   (lambda _Qznxnvf5z5__items: (_Qznxnvf5z5__items[1]))(\n'
                      "   ...     ('foo',\n"
                      "   ...      'bar',),\n"
                      '   ...     ).upper(),\n'
                      '   ...   )\n'
                      "   'BR'\n"
                      '\n'
                      '   #> (.join "" (map &#[#1] \'(abc xyz |123|)))\n'
                      "   >>> ('').join(\n"
                      '   ...   map(\n'
                      "   ...     __import__('functools').partial(\n"
                      '   ...       (lambda _Qznxnvf5z5__items: (_Qznxnvf5z5__items[1])),\n'
                      '   ...       ),\n'
                      "   ...     ('abc',\n"
                      "   ...      'xyz',\n"
                      "   ...      '123',)))\n"
                      "   'by2'\n"
                      '\n'
                      'See also: `\\!# <QzBANG_QzHASH_>`, `-> <QzH_QzGT_>`, `slice`,\n'
                      '`subscriptions`, `slicings`.\n'),
             __name__='QzLSQB_QzHASH_',
             __qualname__='_macro_.QzLSQB_QzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzLSQB_QzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzAT_QzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(
           lambda name,
                  ns=(''):
              (
                (
                  'operator..attrgetter',
                  name,
                  ),
                ns,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``@#`` 'attribute of' Looks up attribute in a namespace.\n"
                      '\n'
                      'Mnemonic: @tribute.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (.join "" (filter @##\'intersection (set "abc") "abracadabra"))\n'
                      "   >>> ('').join(\n"
                      '   ...   filter(\n'
                      "   ...     __import__('operator').attrgetter(\n"
                      "   ...       'intersection')(\n"
                      '   ...       set(\n'
                      "   ...         ('abc'))),\n"
                      "   ...     ('abracadabra')))\n"
                      "   'abacaaba'\n"
                      '\n'
                      "   #> (let (eggs &#@#'upper ; Unary compatible with &#.\n"
                      "   #..      spam 'intersection) ; Lookup need not be constant.\n"
                      "   #..  ;; Various chaining techniques. Note unary @# and '.\n"
                      "   #..  @##'__class__.__name__ (-> (set) @#spam @#'__doc__ eggs))\n"
                      '   >>> # let\n'
                      '   ... (\n'
                      "   ...  lambda eggs=__import__('functools').partial(\n"
                      "   ...           __import__('operator').attrgetter(\n"
                      "   ...             'upper'),\n"
                      '   ...           ),\n'
                      "   ...         spam='intersection':\n"
                      "   ...     __import__('operator').attrgetter(\n"
                      "   ...       '__class__.__name__')(\n"
                      '   ...       # QzH_QzGT_\n'
                      '   ...       eggs(\n'
                      "   ...         __import__('operator').attrgetter(\n"
                      "   ...           '__doc__')(\n"
                      "   ...           __import__('operator').attrgetter(\n"
                      '   ...             spam)(\n'
                      '   ...             set(),\n'
                      '   ...             ),\n'
                      '   ...           )))\n'
                      '   ... )()\n'
                      "   'builtin_function_or_method'\n"
                      '\n'
                      'See also: `getattr`, `operator.attrgetter`, `X# <XQzHASH_>`,\n'
                      '`\\!# <QzBANG_QzHASH_>`, `&# <QzET_QzHASH_>`,\n'
                      '`:@## <QzCOLON_QzAT_QzHASH_>`.\n'),
             __name__='QzAT_QzHASH_',
             __qualname__='_macro_.QzAT_QzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzAT_QzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'setQzBANG_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda items, key, value:
              (
                'hissp.macros.._macro_.let',
                (
                  '_Qzeonpj2u7__value',
                  value,
                  ),
                (
                  'operator..setitem',
                  items,
                  key,
                  '_Qzeonpj2u7__value',
                  ),
                '_Qzeonpj2u7__value',
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``set!`` 'setbang' Assigns an item, returns the value.\n"
                      '\n'
                      'Mnemonic: set !tem.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (define spam (dict))\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   spam=dict())\n'
                      '\n'
                      "   #> (set! spam 1 (set! spam 2 10)) ; setitem can't do this.\n"
                      '   #..\n'
                      '   >>> # setQzBANG_\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      '   ...  lambda _Qzwk5j5q64__value=# setQzBANG_\n'
                      '   ...         # hissp.macros.._macro_.let\n'
                      '   ...         (lambda _Qzwk5j5q64__value=(10):\n'
                      "   ...            (__import__('operator').setitem(\n"
                      '   ...               spam,\n'
                      '   ...               (2),\n'
                      '   ...               _Qzwk5j5q64__value),\n'
                      '   ...             _Qzwk5j5q64__value)  [-1]\n'
                      '   ...         )():\n'
                      "   ...    (__import__('operator').setitem(\n"
                      '   ...       spam,\n'
                      '   ...       (1),\n'
                      '   ...       _Qzwk5j5q64__value),\n'
                      '   ...     _Qzwk5j5q64__value)  [-1]\n'
                      '   ... )()\n'
                      '   10\n'
                      '\n'
                      '   #> spam\n'
                      '   >>> spam\n'
                      '   {2: 10, 1: 10}\n'
                      '\n'
                      'See also: `operator.setitem`, `operator.delitem`, `zap! <zapQzBANG_>`.\n'),
             __name__='setQzBANG_',
             __qualname__='_macro_.setQzBANG_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='setQzBANG_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'zapQzBANG_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda items, key, f, *args:
              (
                'hissp.macros.._macro_.let',
                (
                  '_Qzawhljlfc__items',
                  items,
                  '_Qzawhljlfc__key',
                  key,
                  ),
                (
                  'hissp.macros.._macro_.setQzBANG_',
                  '_Qzawhljlfc__items',
                  '_Qzawhljlfc__key',
                  (
                    f,
                    (
                      '.__getitem__',
                      '_Qzawhljlfc__items',
                      '_Qzawhljlfc__key',
                      ),
                    *args,
                    ),
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``zap!`` 'zapbang' Augmented item assignment operator.\n"
                      '\n'
                      'The current item value becomes the first argument.\n'
                      'Returns the value assigned (not the collection updated).\n'
                      '\n'
                      'Mnemonic: zap !tem.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (define spam (dict : b 10))\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   spam=dict(\n'
                      '   ...          b=(10)))\n'
                      '\n'
                      "   #> (zap! spam 'b op#iadd 1) ; Augmented item assignment, like +=.\n"
                      '   #..\n'
                      '   >>> # zapQzBANG_\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      '   ...  lambda _Qzm6fx4xxk__items=spam,\n'
                      "   ...         _Qzm6fx4xxk__key='b':\n"
                      '   ...     # hissp.macros.._macro_.setQzBANG_\n'
                      '   ...     # hissp.macros.._macro_.let\n'
                      '   ...     (\n'
                      "   ...      lambda _Qzwk5j5q64__value=__import__('operator').iadd(\n"
                      '   ...               _Qzm6fx4xxk__items.__getitem__(\n'
                      '   ...                 _Qzm6fx4xxk__key),\n'
                      '   ...               (1)):\n'
                      "   ...        (__import__('operator').setitem(\n"
                      '   ...           _Qzm6fx4xxk__items,\n'
                      '   ...           _Qzm6fx4xxk__key,\n'
                      '   ...           _Qzwk5j5q64__value),\n'
                      '   ...         _Qzwk5j5q64__value)  [-1]\n'
                      '   ...     )()\n'
                      '   ... )()\n'
                      '   11\n'
                      '\n'
                      '   #> spam\n'
                      '   >>> spam\n'
                      "   {'b': 11}\n"
                      '\n'
                      'See also: `set! <setQzBANG_>`, `zap@ <zapQzAT_>`, `augassign`.\n'),
             __name__='zapQzBANG_',
             __qualname__='_macro_.zapQzBANG_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='zapQzBANG_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'setQzLSQB_QzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda lookup, items, value:
              (
                (
                  'lambda',
                  (
                    '_Qzn6xfsube__items',
                    ':',
                    '_Qzn6xfsube__value',
                    value,
                    ),
                  ('[{v}\n for({}[{})in[{v}]][0]').format(
                    '_Qzn6xfsube__items',
                    __import__('hissp').demunge(
                      lookup),
                    v='_Qzn6xfsube__value'),
                  ),
                items,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``set[###`` 'setsub' Injection. Subscription with assignment.\n"
                      '\n'
                      'Returns the value assigned (not the collection updated).\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (define spam (list "0000"))\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   spam=list(\n'
                      "   ...          ('0000')))\n"
                      '\n'
                      '   #> set[###-1] spam set[###::2] spam "ab" ; Chained assignment.\n'
                      '   >>> (\n'
                      '   ...  lambda _Qzuwg7puku__items,\n'
                      '   ...         _Qzuwg7puku__value=(\n'
                      '   ...          lambda _Qzuwg7puku__items,\n'
                      "   ...                 _Qzuwg7puku__value=('ab'):\n"
                      '   ...             [_Qzuwg7puku__value\n'
                      '   ...              for(_Qzuwg7puku__items[::2])in[_Qzuwg7puku__value]][0]\n'
                      '   ...         )(\n'
                      '   ...           spam):\n'
                      '   ...     [_Qzuwg7puku__value\n'
                      '   ...      for(_Qzuwg7puku__items[-1])in[_Qzuwg7puku__value]][0]\n'
                      '   ... )(\n'
                      '   ...   spam)\n'
                      "   'ab'\n"
                      '\n'
                      '   #> spam\n'
                      '   >>> spam\n'
                      "   ['a', '0', 'b', 'ab']\n"
                      '\n'
                      '``items`` can be ``||`` if set by another macro like `doto`.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (doto (dict) set[###1] || 2)\n'
                      '   >>> # doto\n'
                      '   ... (lambda _Qzogaeaa42__self=dict():\n'
                      '   ...    ((\n'
                      '   ...      lambda _Qzuwg7puku__items,\n'
                      '   ...             _Qzuwg7puku__value=(2):\n'
                      '   ...         [_Qzuwg7puku__value\n'
                      '   ...          for(_Qzuwg7puku__items[1])in[_Qzuwg7puku__value]][0]\n'
                      '   ...     )(\n'
                      '   ...       _Qzogaeaa42__self,\n'
                      '   ...       ),\n'
                      '   ...     _Qzogaeaa42__self)  [-1]\n'
                      '   ... )()\n'
                      '   {1: 2}\n'
                      '\n'
                      'See also: `my# <myQzHASH_>`, `set! <setQzBANG_>`,\n'
                      '`zap[### <zapQzLSQB_QzHASH_>`.\n'),
             __name__='setQzLSQB_QzHASH_',
             __qualname__='_macro_.setQzLSQB_QzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='setQzLSQB_QzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'zapQzLSQB_QzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda lookup, items, callableQzPLUS_args:
              (
                (
                  'lambda',
                  (
                    '_Qzffwqxjac__items',
                    ),
                  (
                    'hissp.macros.._macro_.let',
                    (
                      '_Qzffwqxjac__value',
                      (
                        'hissp.macros..QzMaybe_.QzH_QzGT_',
                        ('({}[{})').format(
                          '_Qzffwqxjac__items',
                          __import__('hissp').demunge(
                            lookup)),
                        callableQzPLUS_args,
                        ),
                      ),
                    ('[{v}\n for({}[{})in[{v}]][0]').format(
                      '_Qzffwqxjac__items',
                      __import__('hissp').demunge(
                        lookup),
                      v='_Qzffwqxjac__value'),
                    ),
                  ),
                items,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``zap[###`` 'zapsub' Injection. Augmented subscription assignment.\n"
                      '\n'
                      'The current item value becomes the first argument.\n'
                      'Returns the value assigned (not the collection updated).\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (define spam (list "abcd"))\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   spam=list(\n'
                      "   ...          ('abcd')))\n"
                      '\n'
                      '   #> zap[###:2] spam (op#iadd "XY")\n'
                      '   >>> (lambda _Qzvibdgdly__items:\n'
                      '   ...     # hissp.macros.._macro_.let\n'
                      '   ...     (\n'
                      '   ...      lambda _Qzvibdgdly__value=# hissp.macros..QzMaybe_.QzH_QzGT_\n'
                      "   ...             __import__('operator').iadd(\n"
                      '   ...               (_Qzvibdgdly__items[:2]),\n'
                      "   ...               ('XY')):\n"
                      '   ...         [_Qzvibdgdly__value\n'
                      '   ...          for(_Qzvibdgdly__items[:2])in[_Qzvibdgdly__value]][0]\n'
                      '   ...     )()\n'
                      '   ... )(\n'
                      '   ...   spam)\n'
                      "   ['a', 'b', 'X', 'Y']\n"
                      '\n'
                      '   #> spam\n'
                      '   >>> spam\n'
                      "   ['a', 'b', 'X', 'Y', 'c', 'd']\n"
                      '\n'
                      '``items`` can be ``||`` if set by another macro like `doto`.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (doto |[2]| zap[###0] || (op#iadd 1))\n'
                      '   >>> # doto\n'
                      '   ... (lambda _Qzogaeaa42__self=[2]:\n'
                      '   ...    ((lambda _Qzvibdgdly__items:\n'
                      '   ...         # hissp.macros.._macro_.let\n'
                      '   ...         (\n'
                      '   ...          lambda _Qzvibdgdly__value=# '
                      'hissp.macros..QzMaybe_.QzH_QzGT_\n'
                      "   ...                 __import__('operator').iadd(\n"
                      '   ...                   (_Qzvibdgdly__items[0]),\n'
                      '   ...                   (1)):\n'
                      '   ...             [_Qzvibdgdly__value\n'
                      '   ...              for(_Qzvibdgdly__items[0])in[_Qzvibdgdly__value]][0]\n'
                      '   ...         )()\n'
                      '   ...     )(\n'
                      '   ...       _Qzogaeaa42__self,\n'
                      '   ...       ),\n'
                      '   ...     _Qzogaeaa42__self)  [-1]\n'
                      '   ... )()\n'
                      '   [3]\n'
                      '\n'
                      '.. CAUTION::\n'
                      '\n'
                      '   The lookup injection must be written twice: once to read and\n'
                      '   once to write. In the unusual case that it has a side effect,\n'
                      '   it will happen twice. Consider `zap! <zapQzBANG_>` instead.\n'
                      '\n'),
             __name__='zapQzLSQB_QzHASH_',
             __qualname__='_macro_.zapQzLSQB_QzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='zapQzLSQB_QzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'setQzAT_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda qualname, value:
              (
                'hissp.macros.._macro_.let',
                (
                  '_Qzgx7xjk5f__value',
                  value,
                  ),
                (
                  'hissp.macros.._macro_.define',
                  qualname,
                  '_Qzgx7xjk5f__value',
                  ),
                '_Qzgx7xjk5f__value',
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``set@`` 'setat' Assigns an attribute, returns the value.\n"
                      '\n'
                      'The namespace part of the ``qualname`` may be fully qualified or start\n'
                      'from a name in scope. An empty namespace part sets an attribute of the\n'
                      'current module (a global).\n'
                      '\n'
                      'Mnemonic: set @tribute.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (set@ eggs (set@ spam (types..SimpleNamespace))) ; define can't do "
                      'this.\n'
                      '   >>> # setQzAT_\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      '   ...  lambda _Qzqfrecvdx__value=# setQzAT_\n'
                      '   ...         # hissp.macros.._macro_.let\n'
                      '   ...         (lambda '
                      "_Qzqfrecvdx__value=__import__('types').SimpleNamespace():\n"
                      '   ...            (# hissp.macros.._macro_.define\n'
                      "   ...             __import__('builtins').globals().update(\n"
                      '   ...               spam=_Qzqfrecvdx__value),\n'
                      '   ...             _Qzqfrecvdx__value)  [-1]\n'
                      '   ...         )():\n'
                      '   ...    (# hissp.macros.._macro_.define\n'
                      "   ...     __import__('builtins').globals().update(\n"
                      '   ...       eggs=_Qzqfrecvdx__value),\n'
                      '   ...     _Qzqfrecvdx__value)  [-1]\n'
                      '   ... )()\n'
                      '   namespace()\n'
                      '\n'
                      '   #> (set@ spam.foo (types..SimpleNamespace))\n'
                      '   >>> # setQzAT_\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      "   ... (lambda _Qzqfrecvdx__value=__import__('types').SimpleNamespace():\n"
                      '   ...    (# hissp.macros.._macro_.define\n'
                      "   ...     __import__('builtins').setattr(\n"
                      '   ...       spam,\n'
                      "   ...       'foo',\n"
                      '   ...       _Qzqfrecvdx__value),\n'
                      '   ...     _Qzqfrecvdx__value)  [-1]\n'
                      '   ... )()\n'
                      '   namespace()\n'
                      '\n'
                      '   #> (set@ spam.foo.bar 4)\n'
                      '   >>> # setQzAT_\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      '   ... (lambda _Qzqfrecvdx__value=(4):\n'
                      '   ...    (# hissp.macros.._macro_.define\n'
                      "   ...     __import__('builtins').setattr(\n"
                      '   ...       spam.foo,\n'
                      "   ...       'bar',\n"
                      '   ...       _Qzqfrecvdx__value),\n'
                      '   ...     _Qzqfrecvdx__value)  [-1]\n'
                      '   ... )()\n'
                      '   4\n'
                      '\n'
                      '   #> spam\n'
                      '   >>> spam\n'
                      '   namespace(foo=namespace(bar=4))\n'
                      '\n'
                      'See also: `attach`, `delattr`, `zap@ <zapQzAT_>`, `setattr`.\n'),
             __name__='setQzAT_',
             __qualname__='_macro_.setQzAT_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='setQzAT_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'zapQzAT_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda qualname, f, *args:
              (
                'hissp.macros.._macro_.setQzAT_',
                qualname,
                (
                  f,
                  # ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    '.' in qualname,
                    (lambda : qualname),
                    (lambda :
                        (
                          '.__getitem__',
                          (
                            'builtins..globals',
                            ),
                          (
                            'quote',
                            qualname,
                            ),
                          )
                    )),
                  *args,
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``zap@`` 'zapat' Augmented attribute assignment operator.\n"
                      '\n'
                      'The current attribute value becomes the first argument.\n'
                      'Returns the value assigned (not the collection updated).\n'
                      '\n'
                      'Mnemonic: zap @tribute.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (define spam (types..SimpleNamespace : foo 10))\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      "   ...   spam=__import__('types').SimpleNamespace(\n"
                      '   ...          foo=(10)))\n'
                      '\n'
                      '   #> (zap@ spam.foo operator..iadd 1)\n'
                      '   >>> # zapQzAT_\n'
                      '   ... # hissp.macros.._macro_.setQzAT_\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      "   ...  lambda _Qzqfrecvdx__value=__import__('operator').iadd(\n"
                      '   ...           spam.foo,\n'
                      '   ...           (1)):\n'
                      '   ...    (# hissp.macros.._macro_.define\n'
                      "   ...     __import__('builtins').setattr(\n"
                      '   ...       spam,\n'
                      "   ...       'foo',\n"
                      '   ...       _Qzqfrecvdx__value),\n'
                      '   ...     _Qzqfrecvdx__value)  [-1]\n'
                      '   ... )()\n'
                      '   11\n'
                      '\n'
                      '   #> spam\n'
                      '   >>> spam\n'
                      '   namespace(foo=11)\n'
                      '\n'
                      "   #> (zap@ spam getattr 'foo)\n"
                      '   >>> # zapQzAT_\n'
                      '   ... # hissp.macros.._macro_.setQzAT_\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      '   ...  lambda _Qzj2zgvjrn__value=getattr(\n'
                      "   ...           __import__('builtins').globals().__getitem__(\n"
                      "   ...             'spam'),\n"
                      "   ...           'foo'):\n"
                      '   ...    (# hissp.macros.._macro_.define\n'
                      "   ...     __import__('builtins').globals().update(\n"
                      '   ...       spam=_Qzj2zgvjrn__value),\n'
                      '   ...     _Qzj2zgvjrn__value)  [-1]\n'
                      '   ... )()\n'
                      '   11\n'
                      '\n'
                      '   #> spam\n'
                      '   >>> spam\n'
                      '   11\n'
                      '\n'
                      'See also: `set@ <setQzAT_>`, `zap! <zapQzBANG_>`, `operator.iadd`,\n'
                      '`augassign`, `:@## <QzCOLON_QzAT_QzHASH_>`.\n'),
             __name__='zapQzAT_',
             __qualname__='_macro_.zapQzAT_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='zapQzAT_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'attach',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda target, *args:
              # let
              (
               lambda iargs=iter(
                        args):
                  # let
                  (
                   lambda args=__import__('itertools').takewhile(
                            (lambda X:
                                __import__('operator').ne(
                                  X,
                                  ':')
                            ),
                            iargs):
                      (
                        'hissp.macros.._macro_.let',
                        (
                          '_Qz4sq7rz5c__target',
                          target,
                          ),
                        *map(
                           (lambda X:
                               (
                                 'builtins..setattr',
                                 '_Qz4sq7rz5c__target',
                                 (
                                   'quote',
                                   X.split('.')[-1],
                                   ),
                                 X,
                                 )
                           ),
                           args),
                        *map(
                           (lambda X:
                               (
                                 'builtins..setattr',
                                 '_Qz4sq7rz5c__target',
                                 (
                                   'quote',
                                   X,
                                   ),
                                 next(
                                   iargs),
                                 )
                           ),
                           iargs),
                        '_Qz4sq7rz5c__target',
                        )
                  )()
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Attaches the named variables to the target as attributes.\n'
                      '\n'
                      'Positional arguments must be identifiers. The identifier name becomes\n'
                      'the attribute name. Names after the ``:`` are identifier-value pairs.\n'
                      'Returns the target.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (attach (types..SimpleNamespace) _macro_.attach : a 1  b 'Hi)\n"
                      '   >>> # attach\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      "   ... (lambda _Qzwg5wn73w__target=__import__('types').SimpleNamespace():\n"
                      "   ...    (__import__('builtins').setattr(\n"
                      '   ...       _Qzwg5wn73w__target,\n'
                      "   ...       'attach',\n"
                      '   ...       _macro_.attach),\n'
                      "   ...     __import__('builtins').setattr(\n"
                      '   ...       _Qzwg5wn73w__target,\n'
                      "   ...       'a',\n"
                      '   ...       (1)),\n'
                      "   ...     __import__('builtins').setattr(\n"
                      '   ...       _Qzwg5wn73w__target,\n'
                      "   ...       'b',\n"
                      "   ...       'Hi'),\n"
                      '   ...     _Qzwg5wn73w__target)  [-1]\n'
                      '   ... )()\n'
                      "   namespace(attach=<function _macro_.attach at 0x...>, a=1, b='Hi')\n"
                      '\n'
                      'See also: `setattr`, `set@ <setQzAT_>`, `vars`.\n'),
             __name__='attach',
             __qualname__='_macro_.attach',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='attach')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'doto',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda self, *invocations:
              (
                (
                  'lambda',
                  (
                    ':',
                    '_Qzbz224liq__self',
                    self,
                    ),
                  *map(
                     (lambda X:
                         (
                           __import__('operator').itemgetter(
                             (0))(
                             X),
                           '_Qzbz224liq__self',
                           *(lambda _Qzud7xb74e__items: (_Qzud7xb74e__items[1:]))(
                              X),
                           )
                     ),
                     map(
                       (lambda X: X if type(X) is tuple else (X,)),
                       invocations)),
                  '_Qzbz224liq__self',
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Configure an object.\n'
                      '\n'
                      'Calls multiple "methods" on one "self".\n'
                      '\n'
                      'Evaluates the given ``self``, then injects it as the first argument to\n'
                      'a sequence of invocations. Returns ``self``.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (doto (list)\n'
                      "   #..  (.extend 'bar)\n"
                      '   #..  .sort\n'
                      "   #..  (.append 'foo))\n"
                      '   >>> # doto\n'
                      '   ... (lambda _Qzkiumbhnz__self=list():\n'
                      '   ...    (_Qzkiumbhnz__self.extend(\n'
                      "   ...       'bar'),\n"
                      '   ...     _Qzkiumbhnz__self.sort(),\n'
                      '   ...     _Qzkiumbhnz__self.append(\n'
                      "   ...       'foo'),\n"
                      '   ...     _Qzkiumbhnz__self)  [-1]\n'
                      '   ... )()\n'
                      "   ['a', 'b', 'r', 'foo']\n"
                      '\n'
                      'See also: `attach`, `progn`, `-> <QzH_QzGT_>`.\n'),
             __name__='doto',
             __qualname__='_macro_.doto',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='doto')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzH_QzGT_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr, *forms:
              __import__('functools').partial(
                __import__('functools').reduce,
                (lambda X, Y: (Y[0],X,*Y[1:],)))(
                map(
                  (lambda X: X if type(X) is tuple else (X,)),
                  forms),
                expr)
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``->`` 'Thread-first'.\n"
                      '\n'
                      'Converts a pipeline to function calls by recursively threading\n'
                      'expressions as the first argument of the next form.\n'
                      'Non-tuple forms (typically function identifiers) will be wrapped\n'
                      'in a tuple. Can make chained method calls easier to read.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (_macro_.-> 'x '(A a) 'B '(C c cc))\n"
                      '   >>> _macro_.QzH_QzGT_(\n'
                      "   ...   'x',\n"
                      "   ...   ('A',\n"
                      "   ...    'a',),\n"
                      "   ...   'B',\n"
                      "   ...   ('C',\n"
                      "   ...    'c',\n"
                      "   ...    'cc',))\n"
                      "   ('C', ('B', ('A', 'x', 'a')), 'c', 'cc')\n"
                      '\n'
                      "   #> (-> 'a set (en#list 'bc) (en#tuple 'de))\n"
                      '   >>> # QzH_QzGT_\n'
                      '   ... (lambda *_Qz6rfwttvx__xs:\n'
                      '   ...     tuple(\n'
                      '   ...       _Qz6rfwttvx__xs)\n'
                      '   ... )(\n'
                      '   ...   (lambda *_Qz6rfwttvx__xs:\n'
                      '   ...       list(\n'
                      '   ...         _Qz6rfwttvx__xs)\n'
                      '   ...   )(\n'
                      '   ...     set(\n'
                      "   ...       'a'),\n"
                      "   ...     'bc'),\n"
                      "   ...   'de')\n"
                      "   ([{'a'}, 'bc'], 'de')\n"
                      '\n'
                      'See also: `-\\<>> <QzH_QzLT_QzGT_QzGT_>`, `X# <XQzHASH_>`,\n'
                      '`\\!# <QzBANG_QzHASH_>`, `en# <enQzHASH_>`.\n'),
             __name__='QzH_QzGT_',
             __qualname__='_macro_.QzH_QzGT_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzH_QzGT_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzH_QzLT_QzGT_QzGT_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr, *forms:
              __import__('functools').partial(
                __import__('functools').reduce,
                (lambda X, Y:
                    # let
                    (
                     lambda i=iter(
                              Y):
                        (
                          *__import__('itertools').takewhile(
                             (lambda X:
                                 __import__('operator').ne(
                                   X,
                                   ':<>')
                             ),
                             i),
                          X,
                          *i,
                          )
                    )()
                ))(
                map(
                  (lambda X: X if type(X) is tuple else (X,)),
                  forms),
                expr)
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``-<>>`` 'Thread-through'.\n"
                      '\n'
                      'Converts a pipeline to function calls by recursively threading\n'
                      'expressions into the next form at the first point indicated with\n'
                      '``:<>``, or at the last if no ``:<>`` is found. Non-tuple forms\n'
                      '(typically function identifiers) will be wrapped in a tuple first.\n'
                      'Can replace partial application in some cases.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (_macro_.-<>>  'x 'A '(:<> b bb) '(C c cc))\n"
                      '   >>> _macro_.QzH_QzLT_QzGT_QzGT_(\n'
                      "   ...   'x',\n"
                      "   ...   'A',\n"
                      "   ...   (':<>',\n"
                      "   ...    'b',\n"
                      "   ...    'bb',),\n"
                      "   ...   ('C',\n"
                      "   ...    'c',\n"
                      "   ...    'cc',))\n"
                      "   ('C', 'c', 'cc', (('A', 'x'), 'b', 'bb'))\n"
                      '\n'
                      "   #> (-<>> 'a set (en#list 'bc) (en#tuple 'de :<> 'fg :<>))\n"
                      '   >>> # QzH_QzLT_QzGT_QzGT_\n'
                      '   ... (lambda *_Qz6rfwttvx__xs:\n'
                      '   ...     tuple(\n'
                      '   ...       _Qz6rfwttvx__xs)\n'
                      '   ... )(\n'
                      "   ...   'de',\n"
                      '   ...   (lambda *_Qz6rfwttvx__xs:\n'
                      '   ...       list(\n'
                      '   ...         _Qz6rfwttvx__xs)\n'
                      '   ...   )(\n'
                      "   ...     'bc',\n"
                      '   ...     set(\n'
                      "   ...       'a')),\n"
                      "   ...   'fg',\n"
                      "   ...   ':<>')\n"
                      "   ('de', ['bc', {'a'}], 'fg', ':<>')\n"
                      '\n'
                      'See also: `-> <QzH_QzGT_>`, `en# <enQzHASH_>`.\n'),
             __name__='QzH_QzLT_QzGT_QzGT_',
             __qualname__='_macro_.QzH_QzLT_QzGT_QzGT_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzH_QzLT_QzGT_QzGT_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# define
__import__('builtins').globals().update(
  _TAO=(lambda s:
           # QzH_QzGT_
           (' ').join(
             __import__('re').findall(
               ('(?m)^# (.*)~$'),
               s(
                 __import__('hissp')))).replace(
             (':'),
             ('\n'))
       ))

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'when',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda condition, *body:
              (
                (
                  'lambda',
                  'bc',
                  'c()if b else()',
                  ),
                condition,
                (
                  'lambda',
                  ':',
                  *body,
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('When the condition is true,\n'
                      'evaluates each expression in sequence for side effects,\n'
                      'resulting in the value of the last.\n'
                      'Otherwise, skips them and returns ``()``.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (any-map c 'abcd\n"
                      '   #..  (print c)\n'
                      "   #..  (when (op#eq c 'b)\n"
                      "   #..    (print 'found)\n"
                      '   #..    :break))\n'
                      '   >>> # anyQzH_map\n'
                      "   ... __import__('builtins').any(\n"
                      "   ...   __import__('builtins').map(\n"
                      '   ...     (lambda c:\n'
                      '   ...        (print(\n'
                      '   ...           c),\n'
                      '   ...         # when\n'
                      '   ...         (lambda b, c: c()if b else())(\n'
                      "   ...           __import__('operator').eq(\n"
                      '   ...             c,\n'
                      "   ...             'b'),\n"
                      '   ...           (lambda :\n'
                      '   ...              (print(\n'
                      "   ...                 'found'),\n"
                      "   ...               ':break')  [-1]\n"
                      '   ...           )))  [-1]\n'
                      '   ...     ),\n'
                      "   ...     'abcd'))\n"
                      '   a\n'
                      '   b\n'
                      '   found\n'
                      '   True\n'
                      '\n'
                      'See also: `if-else <ifQzH_else>`, `unless`, `if`.\n'),
             __name__='when',
             __qualname__='_macro_.when',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='when')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'cond',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda *pairs:
              # when
              (lambda b, c: c()if b else())(
                pairs,
                (lambda :
                    (
                      (
                        'lambda',
                        (
                          *map(
                             (lambda X: f'x{X}'),
                             range(
                               (lambda X: X+1&-2)(
                                 len(
                                   pairs)))),
                          ),
                        __import__('operator').concat(
                          ('\nelse ').join(
                            (
                              ('     x1() if x0'),
                              *map(
                                 (lambda X: f'x{X+1}() if x{X}()'),
                                 range(
                                   (2),
                                   len(
                                     pairs),
                                   (2))),
                              )),
                          ('\nelse ()')),
                        ),
                      __import__('operator').itemgetter(
                        (0))(
                        pairs),
                      *map(
                         (lambda X:
                             (
                               'lambda',
                               ':',
                               X,
                               )
                         ),
                         (lambda _Qzud7xb74e__items: (_Qzud7xb74e__items[1:]))(
                           pairs)),
                      )
                ))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Multiple condition branching.\n'
                      '\n'
                      'Pairs are implied by position. Default is ``()``. Use something always\n'
                      'truthy to change it, like ``:else`` or `True`. For example:\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (any-map x (@ -0.6 -0.0 42.0 math..nan)\n'
                      '   #..  (cond (op#lt x 0) (print :Negative)   ;if-else cascade\n'
                      '   #..        (op#eq x 0) (print :Zero)\n'
                      '   #..        (op#gt x 0) (print :Positive)\n'
                      '   #..        :else (print :Not-a-Number)))\n'
                      '   >>> # anyQzH_map\n'
                      "   ... __import__('builtins').any(\n"
                      "   ...   __import__('builtins').map(\n"
                      '   ...     (lambda x:\n'
                      '   ...         # cond\n'
                      '   ...         (lambda x0, x1, x2, x3, x4, x5, x6, x7:\n'
                      '   ...                  x1() if x0\n'
                      '   ...             else x3() if x2()\n'
                      '   ...             else x5() if x4()\n'
                      '   ...             else x7() if x6()\n'
                      '   ...             else ()\n'
                      '   ...         )(\n'
                      "   ...           __import__('operator').lt(\n"
                      '   ...             x,\n'
                      '   ...             (0)),\n'
                      '   ...           (lambda :\n'
                      '   ...               print(\n'
                      "   ...                 ':Negative')\n"
                      '   ...           ),\n'
                      '   ...           (lambda :\n'
                      "   ...               __import__('operator').eq(\n"
                      '   ...                 x,\n'
                      '   ...                 (0))\n'
                      '   ...           ),\n'
                      '   ...           (lambda :\n'
                      '   ...               print(\n'
                      "   ...                 ':Zero')\n"
                      '   ...           ),\n'
                      '   ...           (lambda :\n'
                      "   ...               __import__('operator').gt(\n"
                      '   ...                 x,\n'
                      '   ...                 (0))\n'
                      '   ...           ),\n'
                      '   ...           (lambda :\n'
                      '   ...               print(\n'
                      "   ...                 ':Positive')\n"
                      '   ...           ),\n'
                      "   ...           (lambda : ':else'),\n"
                      '   ...           (lambda :\n'
                      '   ...               print(\n'
                      "   ...                 ':Not-a-Number')\n"
                      '   ...           ))\n'
                      '   ...     ),\n'
                      '   ...     # QzAT_\n'
                      '   ...     (lambda *xs: [*xs])(\n'
                      '   ...       (-0.6),\n'
                      '   ...       (-0.0),\n'
                      '   ...       (42.0),\n'
                      "   ...       __import__('math').nan)))\n"
                      '   :Negative\n'
                      '   :Zero\n'
                      '   :Positive\n'
                      '   :Not-a-Number\n'
                      '   False\n'
                      '\n'
                      'See also: `if-else <ifQzH_else>`, `case`, `any-map <anyQzH_map>`, `elif`.\n'),
             __name__='cond',
             __qualname__='_macro_.cond',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='cond')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'anyQzH_map',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda variable, xs, *body:
              (
                'builtins..any',
                (
                  'builtins..map',
                  (
                    'lambda',
                    (
                      variable,
                      ),
                    *body,
                    ),
                  xs,
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``any-map`` imperative iterator ``for`` loop.\n'
                      '\n'
                      'Bind the variable and evaluate the body for each ``x`` from ``xs``\n'
                      'until any result is true (and return ``True``), or until ``xs`` is\n'
                      'exhausted (and return ``False``).\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (any-map index (range 1 11)             ;Imperative loop with break.\n'
                      '   #..  (print index : end :)\n'
                      '   #..  (not (op#mod index 7)))\n'
                      '   >>> # anyQzH_map\n'
                      "   ... __import__('builtins').any(\n"
                      "   ...   __import__('builtins').map(\n"
                      '   ...     (lambda index:\n'
                      '   ...        (print(\n'
                      '   ...           index,\n'
                      "   ...           end=':'),\n"
                      '   ...         not(\n'
                      "   ...           __import__('operator').mod(\n"
                      '   ...             index,\n'
                      '   ...             (7))))  [-1]\n'
                      '   ...     ),\n'
                      '   ...     range(\n'
                      '   ...       (1),\n'
                      '   ...       (11))))\n'
                      '   1:2:3:4:5:6:7:True\n'
                      '\n'
                      'See also: `any`, `map`, `any*map <anyQzSTAR_map>`, `for`, `break`,\n'
                      '`functools.reduce`.\n'),
             __name__='anyQzH_map',
             __qualname__='_macro_.anyQzH_map',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='anyQzH_map')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'anyQzSTAR_map',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda variables, xss, *body:
              (
                'builtins..any',
                (
                  'itertools..starmap',
                  (
                    'lambda',
                    variables,
                    *body,
                    ),
                  xss,
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``any*map`` 'any star map' imperative iterator ``for`` loop & unpack.\n"
                      '\n'
                      'Bind each ``x`` to a variable and evaluate the body for each ``xs``\n'
                      'from ``xss`` until any result is true (and return ``True``), or\n'
                      'until ``xss`` is exhausted (and return ``False``).\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (any*map (i c) (enumerate 'abc 1)  ; As any-map, but with starmap.\n"
                      '   #..  (print (op#mul i c)))\n'
                      '   >>> # anyQzSTAR_map\n'
                      "   ... __import__('builtins').any(\n"
                      "   ...   __import__('itertools').starmap(\n"
                      '   ...     (lambda i, c:\n'
                      '   ...         print(\n'
                      "   ...           __import__('operator').mul(\n"
                      '   ...             i,\n'
                      '   ...             c))\n'
                      '   ...     ),\n'
                      '   ...     enumerate(\n'
                      "   ...       'abc',\n"
                      '   ...       (1))))\n'
                      '   a\n'
                      '   bb\n'
                      '   ccc\n'
                      '   False\n'
                      '\n'
                      'See also: `itertools.starmap`, `any-map <anyQzH_map>`,\n'
                      '`loop-from <loopQzH_from>`, `let*from <letQzSTAR_from>`,\n'
                      '`my# <myQzHASH_>`.\n'),
             __name__='anyQzSTAR_map',
             __qualname__='_macro_.anyQzSTAR_map',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='anyQzSTAR_map')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'loopQzH_from',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda syms, inits, *body:
              (
                'hissp.macros.._macro_.let',
                (
                  '_Qzhpagmhdx__stack',
                  (
                    'hissp.macros..QzMaybe_.QzAT_',
                    (),
                    None,
                    inits,
                    ),
                  ),
                (
                  'hissp.macros.._macro_.let',
                  (
                    'recurQzH_from',
                    '_Qzhpagmhdx__stack.append',
                    ),
                  (
                    'hissp.macros.._macro_.anyQzSTAR_map',
                    syms,
                    (
                      'builtins..iter',
                      '_Qzhpagmhdx__stack.pop',
                      None,
                      ),
                    (
                      '.__setitem__',
                      '_Qzhpagmhdx__stack',
                      (0),
                      (
                        'hissp.macros.._macro_.progn',
                        *body,
                        ),
                      ),
                    None,
                    ),
                  (
                    (
                      'operator..itemgetter',
                      (0),
                      ),
                    '_Qzhpagmhdx__stack',
                    ),
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``loop-from`` Anaphoric. Loop/recur with trampoline.\n'
                      '\n'
                      'Set local values for the first loop with an iterable as\n'
                      '`let-from <letQzH_from>`.\n'
                      '\n'
                      'Creates a stack to schedule future loops. Call the ``recur-from``\n'
                      'anaphor with an iterable of values for the locals to push another loop\n'
                      'to the schedule. Call with ``None`` to abort any remaining schedule.\n'
                      '\n'
                      'Returns the value of the final loop.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (loop-from x '(3)                       ;Unpacks as let-from.\n"
                      '   #..  (when x\n'
                      '   #..    (print x)\n'
                      '   #..    (recur-from (@ (op#sub x 1)))))\n'
                      '   >>> # loopQzH_from\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      '   ...  lambda _Qzj54t3dhw__stack=# hissp.macros..QzMaybe_.QzAT_\n'
                      '   ...         (lambda *xs: [*xs])(\n'
                      '   ...           (),\n'
                      '   ...           None,\n'
                      '   ...           ((3),)):\n'
                      '   ...     # hissp.macros.._macro_.let\n'
                      '   ...     (lambda recurQzH_from=_Qzj54t3dhw__stack.append:\n'
                      '   ...        (# hissp.macros.._macro_.anyQzSTAR_map\n'
                      "   ...         __import__('builtins').any(\n"
                      "   ...           __import__('itertools').starmap(\n"
                      '   ...             (lambda x:\n'
                      '   ...                (_Qzj54t3dhw__stack.__setitem__(\n'
                      '   ...                   (0),\n'
                      '   ...                   # hissp.macros.._macro_.progn\n'
                      '   ...                   # when\n'
                      '   ...                   (lambda b, c: c()if b else())(\n'
                      '   ...                     x,\n'
                      '   ...                     (lambda :\n'
                      '   ...                        (print(\n'
                      '   ...                           x),\n'
                      '   ...                         recurQzH_from(\n'
                      '   ...                           # QzAT_\n'
                      '   ...                           (lambda *xs: [*xs])(\n'
                      "   ...                             __import__('operator').sub(\n"
                      '   ...                               x,\n'
                      '   ...                               (1)))))  [-1]\n'
                      '   ...                     ))),\n'
                      '   ...                 None)  [-1]\n'
                      '   ...             ),\n'
                      "   ...             __import__('builtins').iter(\n"
                      '   ...               _Qzj54t3dhw__stack.pop,\n'
                      '   ...               None))),\n'
                      "   ...         __import__('operator').itemgetter(\n"
                      '   ...           (0))(\n'
                      '   ...           _Qzj54t3dhw__stack))  [-1]\n'
                      '   ...     )()\n'
                      '   ... )()\n'
                      '   3\n'
                      '   2\n'
                      '   1\n'
                      '   ()\n'
                      '\n'
                      'See also: `any*map <anyQzSTAR_map>`, `Ensue`_, `while`.\n'),
             __name__='loopQzH_from',
             __qualname__='_macro_.loopQzH_from',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='loopQzH_from')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'ands',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda *exprs:
              # cond
              (lambda x0, x1, x2, x3, x4, x5:
                       x1() if x0
                  else x3() if x2()
                  else x5() if x4()
                  else ()
              )(
                not(
                  exprs),
                (lambda : True),
                (lambda :
                    __import__('operator').eq(
                      len(
                        exprs),
                      (1))
                ),
                (lambda :
                    __import__('operator').itemgetter(
                      (0))(
                      exprs)
                ),
                (lambda : ':else'),
                (lambda :
                    (
                      (
                        'lambda',
                        (
                          *map(
                             (lambda X: f'x{X}'),
                             range(
                               len(
                                 exprs))),
                          ),
                        ('and ').join(
                          (
                            ('x0 '),
                            *map(
                               (lambda X: f'x{X}()'),
                               range(
                                 (1),
                                 len(
                                   exprs))),
                            )),
                        ),
                      __import__('operator').itemgetter(
                        (0))(
                        exprs),
                      *map(
                         (lambda X:
                             (
                               'lambda',
                               ':',
                               X,
                               )
                         ),
                         (lambda _Qzud7xb74e__items: (_Qzud7xb74e__items[1:]))(
                           exprs)),
                      )
                ))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Variadic shortcutting logical AND.\n'
                      '\n'
                      'Returns the first false value, otherwise the last value.\n'
                      'There is an implicit initial value of ``True``.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (ands True True False) ; and finds the False\n'
                      '   >>> # ands\n'
                      '   ... (lambda x0, x1, x2: x0 and x1()and x2())(\n'
                      '   ...   True,\n'
                      '   ...   (lambda : True),\n'
                      '   ...   (lambda : False))\n'
                      '   False\n'
                      '\n'
                      "   #> (ands False (print 'oops)) ; Shortcutting.\n"
                      '   >>> # ands\n'
                      '   ... (lambda x0, x1: x0 and x1())(\n'
                      '   ...   False,\n'
                      '   ...   (lambda :\n'
                      '   ...       print(\n'
                      "   ...         'oops')\n"
                      '   ...   ))\n'
                      '   False\n'
                      '\n'
                      '   #> (ands True 42)\n'
                      '   >>> # ands\n'
                      '   ... (lambda x0, x1: x0 and x1())(\n'
                      '   ...   True,\n'
                      '   ...   (lambda : (42)))\n'
                      '   42\n'
                      '\n'
                      '   #> (ands)\n'
                      '   >>> # ands\n'
                      '   ... True\n'
                      '   True\n'
                      '\n'
                      '   #> (ands 42)\n'
                      '   >>> # ands\n'
                      '   ... (42)\n'
                      '   42\n'
                      '\n'
                      'See also: `ors`, `and`, `all`, `when`.\n'),
             __name__='ands',
             __qualname__='_macro_.ands',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='ands')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'ors',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda *exprs:
              # cond
              (lambda x0, x1, x2, x3:
                       x1() if x0
                  else x3() if x2()
                  else ()
              )(
                __import__('operator').eq(
                  len(
                    exprs),
                  (1)),
                (lambda :
                    __import__('operator').itemgetter(
                      (0))(
                      exprs)
                ),
                (lambda : exprs),
                (lambda :
                    (
                      (
                        'lambda',
                        (
                          *map(
                             (lambda X: f'x{X}'),
                             range(
                               len(
                                 exprs))),
                          ),
                        ('or ').join(
                          (
                            ('x0 '),
                            *map(
                               (lambda X: f'x{X}()'),
                               range(
                                 (1),
                                 len(
                                   exprs))),
                            )),
                        ),
                      __import__('operator').itemgetter(
                        (0))(
                        exprs),
                      *map(
                         (lambda X:
                             (
                               'lambda',
                               ':',
                               X,
                               )
                         ),
                         (lambda _Qzud7xb74e__items: (_Qzud7xb74e__items[1:]))(
                           exprs)),
                      )
                ))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Variadic shortcutting logical OR.\n'
                      '\n'
                      'Returns the first true value, otherwise the last value.\n'
                      'There is an implicit initial value of ``()``.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (ors True (print 'oops)) ; Shortcutting.\n"
                      '   >>> # ors\n'
                      '   ... (lambda x0, x1: x0 or x1())(\n'
                      '   ...   True,\n'
                      '   ...   (lambda :\n'
                      '   ...       print(\n'
                      "   ...         'oops')\n"
                      '   ...   ))\n'
                      '   True\n'
                      '\n'
                      '   #> (ors 42 False)\n'
                      '   >>> # ors\n'
                      '   ... (lambda x0, x1: x0 or x1())(\n'
                      '   ...   (42),\n'
                      '   ...   (lambda : False))\n'
                      '   42\n'
                      '\n'
                      '   #> (ors () False 0 1)  ; or seeks the truth\n'
                      '   >>> # ors\n'
                      '   ... (lambda x0, x1, x2, x3: x0 or x1()or x2()or x3())(\n'
                      '   ...   (),\n'
                      '   ...   (lambda : False),\n'
                      '   ...   (lambda : (0)),\n'
                      '   ...   (lambda : (1)))\n'
                      '   1\n'
                      '\n'
                      '   #> (ors False)\n'
                      '   >>> # ors\n'
                      '   ... False\n'
                      '   False\n'
                      '\n'
                      '   #> (ors)\n'
                      '   >>> # ors\n'
                      '   ... ()\n'
                      '   ()\n'
                      '\n'
                      'See also: `ands`, `bool`, `or`, `any`.\n'),
             __name__='ors',
             __qualname__='_macro_.ors',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='ors')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'throwQzSTAR_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda *exception:
              (
                "(lambda g:g.close()or g.throw)(c for c in'')",
                *exception,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``throw*`` 'throw star' Creates a closed generator and calls ``.throw``.\n"
                      '\n'
                      'Despite `PEP 3109 <https://peps.python.org/pep-3109/>`_, ``.throw``\n'
                      'still seems to accept multiple arguments. Avoid using this form\n'
                      'except when implementing throw method overrides. Prefer `throw`\n'
                      'instead.\n'
                      '\n'
                      'The 3-arg form is deprecated as of Python 3.12.\n'),
             __name__='throwQzSTAR_',
             __qualname__='_macro_.throwQzSTAR_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='throwQzSTAR_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'throw',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda exception:
              (
                'hissp.macros.._macro_.throwQzSTAR_',
                exception,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Raise an exception.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (throw Exception)                       ;Raise exception objects or '
                      'classes.\n'
                      '   >>> # throw\n'
                      '   ... # hissp.macros.._macro_.throwQzSTAR_\n'
                      "   ... (lambda g:g.close()or g.throw)(c for c in'')(\n"
                      '   ...   Exception)\n'
                      '   Traceback (most recent call last):\n'
                      '     ...\n'
                      '   Exception\n'
                      '\n'
                      "   #> (throw (TypeError 'message))\n"
                      '   >>> # throw\n'
                      '   ... # hissp.macros.._macro_.throwQzSTAR_\n'
                      "   ... (lambda g:g.close()or g.throw)(c for c in'')(\n"
                      '   ...   TypeError(\n'
                      "   ...     'message'))\n"
                      '   Traceback (most recent call last):\n'
                      '     ...\n'
                      '   TypeError: message\n'
                      '\n'
                      'See also: `throw-from <throwQzH_from>`, `engarde`_, `raise`.\n'),
             __name__='throw',
             __qualname__='_macro_.throw',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='throw')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'throwQzH_from',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda exception, cause:
              (
                'hissp.macros.._macro_.throwQzSTAR_',
                (
                  'hissp.macros.._macro_.let',
                  (
                    '_Qzkmnhayfp__G',
                    (
                      'lambda',
                      (
                        '_Qzkmnhayfp__x',
                        ),
                      (
                        'hissp.macros.._macro_.ifQzH_else',
                        (
                          'builtins..isinstance',
                          '_Qzkmnhayfp__x',
                          'builtins..BaseException',
                          ),
                        '_Qzkmnhayfp__x',
                        (
                          '_Qzkmnhayfp__x',
                          ),
                        ),
                      ),
                    ),
                  (
                    'hissp.macros.._macro_.attach',
                    (
                      '_Qzkmnhayfp__G',
                      exception,
                      ),
                    ':',
                    '__cause__',
                    (
                      '_Qzkmnhayfp__G',
                      cause,
                      ),
                    ),
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``throw-from`` Raise an exception with a cause, which can be None.\n'
                      '\n'
                      'If ``exception`` is not an instance of `BaseException`, it will be\n'
                      'presumed an exception class and called with no arguments before\n'
                      'attaching the cause to the resulting instance.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (throw-from Exception (Exception 'message)) ; Explicit chaining.\n"
                      '   #..\n'
                      '   >>> # throwQzH_from\n'
                      '   ... # hissp.macros.._macro_.throwQzSTAR_\n'
                      "   ... (lambda g:g.close()or g.throw)(c for c in'')(\n"
                      '   ...   # hissp.macros.._macro_.let\n'
                      '   ...   (\n'
                      '   ...    lambda _Qzzkusd5eu__G=(lambda _Qzzkusd5eu__x:\n'
                      '   ...               # hissp.macros.._macro_.ifQzH_else\n'
                      '   ...               (lambda b, c, a: c()if b else a())(\n'
                      "   ...                 __import__('builtins').isinstance(\n"
                      '   ...                   _Qzzkusd5eu__x,\n'
                      "   ...                   __import__('builtins').BaseException),\n"
                      '   ...                 (lambda : _Qzzkusd5eu__x),\n'
                      '   ...                 (lambda : _Qzzkusd5eu__x()))\n'
                      '   ...           ):\n'
                      '   ...       # hissp.macros.._macro_.attach\n'
                      '   ...       # hissp.macros.._macro_.let\n'
                      '   ...       (\n'
                      '   ...        lambda _Qzwawunnb6__target=_Qzzkusd5eu__G(\n'
                      '   ...                 Exception):\n'
                      "   ...          (__import__('builtins').setattr(\n"
                      '   ...             _Qzwawunnb6__target,\n'
                      "   ...             '__cause__',\n"
                      '   ...             _Qzzkusd5eu__G(\n'
                      '   ...               Exception(\n'
                      "   ...                 'message'))),\n"
                      '   ...           _Qzwawunnb6__target)  [-1]\n'
                      '   ...       )()\n'
                      '   ...   )())\n'
                      '   Traceback (most recent call last):\n'
                      '     ...\n'
                      '   Exception\n'
                      '\n'
                      'See also: `throw`, `throw* <throwQzSTAR_>`.\n'),
             __name__='throwQzH_from',
             __qualname__='_macro_.throwQzH_from',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='throwQzH_from')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'prog1',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr1, *body:
              (
                'hissp.macros.._macro_.let',
                (
                  '_Qzy4a7j2tp__value1',
                  expr1,
                  ),
                *body,
                '_Qzy4a7j2tp__value1',
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Evaluates sequentially (for side effects). Returns value of ``expr1``.\n'
                      '\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (print (prog1 0                         ;Side effects in sequence. '
                      'Eval to first.\n'
                      '   #..         (print 1)\n'
                      '   #..         (print 2)))\n'
                      '   >>> print(\n'
                      '   ...   # prog1\n'
                      '   ...   # hissp.macros.._macro_.let\n'
                      '   ...   (lambda _Qz46bj7iw6__value1=(0):\n'
                      '   ...      (print(\n'
                      '   ...         (1)),\n'
                      '   ...       print(\n'
                      '   ...         (2)),\n'
                      '   ...       _Qz46bj7iw6__value1)  [-1]\n'
                      '   ...   )())\n'
                      '   1\n'
                      '   2\n'
                      '   0\n'
                      '\n'
                      'Combine with `progn` for a value in the middle of the sequence:\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (prog1                                  ;Side effects in sequence. '
                      'Eval to first.\n'
                      '   #..  (progn (print 1)                      ;Side effects in sequence. '
                      'Eval to last.\n'
                      '   #..         3)\n'
                      '   #..  (print 2))\n'
                      '   >>> # prog1\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      '   ...  lambda _Qz46bj7iw6__value1=# progn\n'
                      '   ...         (print(\n'
                      '   ...            (1)),\n'
                      '   ...          (3))  [-1]:\n'
                      '   ...    (print(\n'
                      '   ...       (2)),\n'
                      '   ...     _Qz46bj7iw6__value1)  [-1]\n'
                      '   ... )()\n'
                      '   1\n'
                      '   2\n'
                      '   3\n'
                      '\n'
                      'See also: `doto`.\n'),
             __name__='prog1',
             __qualname__='_macro_.prog1',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='prog1')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'bQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda string:
              # QzH_QzGT_
              __import__('ast').literal_eval(
                # QzH_QzLT_QzGT_QzGT_
                ("b'{}'").format(
                  __import__('ast').literal_eval(
                    __import__('hissp').readerless(
                      string)).replace(
                    ("'"),
                    "\\'").replace(
                    ('\n'),
                    '\\n')))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``b#`` 'bytestring' bytes literal tag\n"
                      '\n'
                      'Converts a `Hissp string` to `bytes`.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> b#"bytes\n'
                      '   #..with\\nnewlines"\n'
                      "   >>> b'bytes\\nwith\\nnewlines'\n"
                      "   b'bytes\\nwith\\nnewlines'\n"
                      '\n'
                      '\n'
                      "   #> b#'bytes! ; Note the '. Beware munging.\n"
                      "   >>> b'bytesQzBANG_'\n"
                      "   b'bytesQzBANG_'\n"
                      '\n'
                      '   #> b#<#\n'
                      '   #..;; Bytes,\n'
                      '   #..;; newlines, \\46 escapes!\n'
                      '   #..\n'
                      "   >>> b'Bytes,\\nnewlines, & escapes!'\n"
                      "   b'Bytes,\\nnewlines, & escapes!'\n"
                      '\n'
                      'See also: `B# <BQzHASH_>`, `hissp.reader.is_hissp_string`.\n'),
             __name__='bQzHASH_',
             __qualname__='_macro_.bQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='bQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'BQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda symbol:
              # QzH_QzGT_
              __import__('ast').literal_eval(
                # QzH_QzLT_QzGT_QzGT_
                ("b'{}'").format(
                  symbol.replace(
                    ("'"),
                    "\\'").replace(
                    ('\n'),
                    '\\n')))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``B#`` 'bytesymbol'\n"
                      '\n'
                      'Converts a `parsed object` of type `str` to `bytes`.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> B#|bytes!|\n'
                      "   >>> b'bytes!'\n"
                      "   b'bytes!'\n"
                      '\n'
                      '   #> B#oops! ; Works directly on symbols, but beware munging.\n'
                      "   >>> b'oopsQzBANG_'\n"
                      "   b'oopsQzBANG_'\n"
                      '\n'
                      '   #> B#"oops!" ; You probably wanted b# instead.\n'
                      '   >>> b"(\'oops!\')"\n'
                      '   b"(\'oops!\')"\n'
                      '\n'
                      '   #> B#.#"OK" ; Note the .#.\n'
                      "   >>> b'OK'\n"
                      "   b'OK'\n"
                      '\n'
                      '   #> B#|\\xff || "\\n\'" BBQ| ; Escapes allowed, like b#.\n'
                      '   >>> b\'\\xff | "\\n\\\'" BBQ\'\n'
                      '   b\'\\xff | "\\n\\\'" BBQ\'\n'
                      '\n'
                      'See also: `b# <bQzHASH_>`.\n'),
             __name__='BQzHASH_',
             __qualname__='_macro_.BQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='BQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda Q:
              __import__('fractions').Fraction(
                __import__('hissp').demunge(
                  Q))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``Q#`` 'Rational' Exact fraction tag.\n"
                      '\n'
                      'Abbreviation for `fractions.Fraction`, with a `demunge` for symbols.\n'
                      '\n'
                      'Mnemonic: ℚuotient.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> Q#2/3\n'
                      '   >>> # Fraction(2, 3)\n'
                      "   ... __import__('pickle').loads(b'cfractions\\nFraction\\n(V2/3\\ntR.')\n"
                      '   Fraction(2, 3)\n'
                      '\n'
                      'See also: `M# <MQzHASH_>`.\n'),
             __name__='QQzHASH_',
             __qualname__='_macro_.QQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'MQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda M:
              __import__('decimal').Decimal(
                __import__('hissp').demunge(
                  M))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``M#`` 'Decimal' Exact decimal tag.\n"
                      '\n'
                      'Abbreviation for `decimal.Decimal`, with a `demunge` for symbols.\n'
                      '\n'
                      'Mnemonic: "Money". Chosen to resemble Clojure\'s ``BigDecimal``\n'
                      'literal, likely inspired by C♯ where "D" was taken for\n'
                      'double-precision floats, leaving "M" as the next best letter in\n'
                      '"deciMal".\n'
                      '\n'
                      'The usual construction has a trailing underscore to avoid going\n'
                      'through a float literal, which would have limited precision:\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> M#1.23e6_\n'
                      "   >>> # Decimal('1.23E+6')\n"
                      "   ... __import__('pickle').loads(b'cdecimal\\nDecimal\\n(V1.23E+6\\ntR.')\n"
                      "   Decimal('1.23E+6')\n"
                      '\n'
                      'When converting a read-time constant float, go through `str` first:\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> M#.#(repr math..tau)\n'
                      "   >>> # Decimal('6.283185307179586')\n"
                      '   ... '
                      "__import__('pickle').loads(b'cdecimal\\nDecimal\\n(V6.283185307179586\\ntR.')\n"
                      "   Decimal('6.283185307179586')\n"
                      '\n'
                      'See also: `Q# <QQzHASH_>`.\n'),
             __name__='MQzHASH_',
             __qualname__='_macro_.MQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='MQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'instQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda date_string:
              __import__('datetime').datetime.fromisoformat(
                __import__('hissp').demunge(
                  date_string))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``inst#`` instant tag.\n'
                      '\n'
                      'Abbreviation for `datetime.datetime.fromisoformat`,\n'
                      'with a `demunge` for symbols.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> inst#2024-10-07T11:30:07+00:00\n'
                      '   >>> # datetime.datetime(2024, 10, 7, 11, 30, 7, '
                      'tzinfo=datetime.timezone.utc)\n'
                      '   ... '
                      "__import__('pickle').loads(b'cdatetime\\ndatetime\\n(c_codecs\\nencode\\n(V\\x07\\xe8\\\\u000a\\x07\\x0b\\x1e\\x07\\\\u0000\\\\u0000\\\\u0000\\nVlatin1\\ntRcdatetime\\ntimezone\\n(cdatetime\\ntimedelta\\n(I0\\nI0\\nI0\\ntRtRtR.')\n"
                      '   datetime.datetime(2024, 10, 7, 11, 30, 7, tzinfo=datetime.timezone.utc)\n'
                      '\n'
                      '\n'
                      'See also: `uuid# <uuidQzHASH_>`.\n'),
             __name__='instQzHASH_',
             __qualname__='_macro_.instQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='instQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'uuidQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda hex:
              __import__('uuid').UUID(
                __import__('hissp').demunge(
                  hex))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``uuid#`` Universally Unique Identifier tag.\n'
                      '\n'
                      'Abbreviation for `uuid.UUID`, with a `demunge` for symbols.\n'
                      'Curly braces, hyphens, and a URN prefix are optional,\n'
                      'but the argument must be a read-time `str`, not an `int`.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> uuid#{urn:uuid:12345678-1234-5678-1234-567812345678}\n'
                      "   >>> # UUID('12345678-1234-5678-1234-567812345678')\n"
                      '   ... '
                      "__import__('pickle').loads(b'ccopy_reg\\n_reconstructor\\n(cuuid\\nUUID\\nc__builtin__\\nobject\\nNtR(dVint\\nL24197857161011715162171839636988778104L\\nsb.')\n"
                      "   UUID('12345678-1234-5678-1234-567812345678')\n"
                      '\n'
                      'See also: `inst# <instQzHASH_>`.\n'),
             __name__='uuidQzHASH_',
             __qualname__='_macro_.uuidQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='uuidQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'enQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda f:
              # ifQzH_else
              (lambda b, c, a: c()if b else a())(
                # ands
                (lambda x0, x1: x0 and x1())(
                  __import__('operator').is_(
                    str,
                    type(
                      f)),
                  (lambda :
                      f.startswith(
                        ('.'))
                  )),
                (lambda :
                    (
                      'lambda',
                      (
                        '_Qzkmrxf6tz__self',
                        ':',
                        ':*',
                        '_Qzkmrxf6tz__xs',
                        ),
                      (
                        f,
                        '_Qzkmrxf6tz__self',
                        '_Qzkmrxf6tz__xs',
                        ),
                      )
                ),
                (lambda :
                    (
                      'lambda',
                      (
                        ':',
                        ':*',
                        '_Qzuzudkt6p__xs',
                        ),
                      (
                        f,
                        '_Qzuzudkt6p__xs',
                        ),
                      )
                ))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``en#`` tag.\n'
                      'Wrap a function applicable to a tuple as a function of its elements.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (en#list 1 2 3)\n'
                      '   >>> (lambda *_Qz6rfwttvx__xs:\n'
                      '   ...     list(\n'
                      '   ...       _Qz6rfwttvx__xs)\n'
                      '   ... )(\n'
                      '   ...   (1),\n'
                      '   ...   (2),\n'
                      '   ...   (3))\n'
                      '   [1, 2, 3]\n'
                      '\n'
                      '   #> (en#.extend _ 4 5 6) ; Methods too.\n'
                      '   #..\n'
                      '   >>> (lambda _Qz6rfwttvx__self, *_Qz6rfwttvx__xs:\n'
                      '   ...     _Qz6rfwttvx__self.extend(\n'
                      '   ...       _Qz6rfwttvx__xs)\n'
                      '   ... )(\n'
                      '   ...   _,\n'
                      '   ...   (4),\n'
                      '   ...   (5),\n'
                      '   ...   (6))\n'
                      '\n'
                      '   #> _\n'
                      '   >>> _\n'
                      '   [1, 2, 3, 4, 5, 6]\n'
                      '\n'
                      '   #> (define enjoin en#X#(.join "" (map str X)))\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   enjoin=(lambda *_Qz6rfwttvx__xs:\n'
                      '   ...              (lambda X:\n'
                      "   ...                  ('').join(\n"
                      '   ...                    map(\n'
                      '   ...                      str,\n'
                      '   ...                      X))\n'
                      '   ...              )(\n'
                      '   ...                _Qz6rfwttvx__xs)\n'
                      '   ...          ))\n'
                      '\n'
                      '   #> (enjoin "Sum: "(op#add 2 3)". Product: "(op#mul 2 3)".")\n'
                      '   >>> enjoin(\n'
                      "   ...   ('Sum: '),\n"
                      "   ...   __import__('operator').add(\n"
                      '   ...     (2),\n'
                      '   ...     (3)),\n'
                      "   ...   ('. Product: '),\n"
                      "   ...   __import__('operator').mul(\n"
                      '   ...     (2),\n'
                      '   ...     (3)),\n'
                      "   ...   ('.'))\n"
                      "   'Sum: 5. Product: 6.'\n"
                      '\n'
                      'There are no bundled tags for a quinary, senary, etc. but\n'
                      'the ``en#X#`` variadic or a normal lambda form can be used instead.\n'
                      '\n'
                      'See also:\n'
                      '`X# <XQzHASH_>`, `&# <QzET_QzHASH_>`, `/# <QzSOL_QzHASH_>`, `@ <QzAT_>`.\n'),
             __name__='enQzHASH_',
             __qualname__='_macro_.enQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='enQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzSOL_QzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda f:
              (
                'lambda',
                (
                  ':',
                  ':*',
                  '_Qzkhzy2scs__xs',
                  ),
                (
                  'functools..reduce',
                  f,
                  '_Qzkhzy2scs__xs',
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``/#`` 'reduce by' Wrap a binary function as a variadic via reduce.\n"
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (/#operator..add 1 2 3 4)\n'
                      '   >>> (lambda *_Qztkr22wce__xs:\n'
                      "   ...     __import__('functools').reduce(\n"
                      "   ...       __import__('operator').add,\n"
                      '   ...       _Qztkr22wce__xs)\n'
                      '   ... )(\n'
                      '   ...   (1),\n'
                      '   ...   (2),\n'
                      '   ...   (3),\n'
                      '   ...   (4))\n'
                      '   10\n'
                      '\n'
                      'See also: `/XY# <QzSOL_XYQzHASH_>`, `en# <enQzHASH_>`.'),
             __name__='QzSOL_QzHASH_',
             __qualname__='_macro_.QzSOL_QzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzSOL_QzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'proxyQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda f:
              (
                'functools..update_wrapper',
                (
                  'lambda',
                  (
                    ':',
                    ':*',
                    '_Qzm4elr2f6__args',
                    ':**',
                    '_Qzm4elr2f6__kwargs',
                    ),
                  (
                    f,
                    ':',
                    ':*',
                    '_Qzm4elr2f6__args',
                    ':**',
                    '_Qzm4elr2f6__kwargs',
                    ),
                  ),
                f,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``proxy#`` wrapper to make a stored callable reloadable.\n'
                      '\n'
                      'For this to work, it should be applied to a lookup expression\n'
                      'such as a global variable name or module attribute.\n'
                      'This will be written into the wrapper body.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (defun greet ()\n'
                      '   #..  (print "Hello, World!"))\n'
                      '   >>> # defun\n'
                      '   ... # hissp.macros.._macro_.define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   greet=# hissp.macros.._macro_.fun\n'
                      '   ...         # hissp.macros.._macro_.let\n'
                      '   ...         (\n'
                      '   ...          lambda _Qzan3nwcb3__lambda=(lambda :\n'
                      '   ...                     print(\n'
                      "   ...                       ('Hello, World!'))\n"
                      '   ...                 ):\n'
                      '   ...            ((\n'
                      "   ...               *__import__('itertools').starmap(\n"
                      '   ...                  _Qzan3nwcb3__lambda.__setattr__,\n'
                      "   ...                  __import__('builtins').dict(\n"
                      "   ...                    __name__='greet',\n"
                      "   ...                    __qualname__='greet',\n"
                      '   ...                    __code__=_Qzan3nwcb3__lambda.__code__.replace(\n'
                      "   ...                               co_name='greet')).items()),\n"
                      '   ...               ),\n'
                      '   ...             _Qzan3nwcb3__lambda)  [-1]\n'
                      '   ...         )())\n'
                      '\n'
                      '   #> proxy#greet\n'
                      "   >>> __import__('functools').update_wrapper(\n"
                      '   ...   (lambda *_Qzxd2las5y__args, **_Qzxd2las5y__kwargs:\n'
                      '   ...       greet(\n'
                      '   ...         *_Qzxd2las5y__args,\n'
                      '   ...         **_Qzxd2las5y__kwargs)\n'
                      '   ...   ),\n'
                      '   ...   greet)\n'
                      '   <function greet at 0x...>\n'
                      '\n'
                      '   #> (define greet-handlers (types..SimpleNamespace : direct greet  proxied '
                      '_))\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      "   ...   greetQzH_handlers=__import__('types').SimpleNamespace(\n"
                      '   ...                       direct=greet,\n'
                      '   ...                       proxied=_))\n'
                      '\n'
                      'Now suppose ``greet`` is reloaded with a new definition, but\n'
                      '``greet-handlers`` is not (perhaps due to being in separate modules\n'
                      'or if ``greet-handlers`` had used `defonce`):\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (defun greet ()\n'
                      '   #..  (print "Wassup?"))\n'
                      '   >>> # defun\n'
                      '   ... # hissp.macros.._macro_.define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   greet=# hissp.macros.._macro_.fun\n'
                      '   ...         # hissp.macros.._macro_.let\n'
                      '   ...         (\n'
                      '   ...          lambda _Qzan3nwcb3__lambda=(lambda :\n'
                      '   ...                     print(\n'
                      "   ...                       ('Wassup?'))\n"
                      '   ...                 ):\n'
                      '   ...            ((\n'
                      "   ...               *__import__('itertools').starmap(\n"
                      '   ...                  _Qzan3nwcb3__lambda.__setattr__,\n'
                      "   ...                  __import__('builtins').dict(\n"
                      "   ...                    __name__='greet',\n"
                      "   ...                    __qualname__='greet',\n"
                      '   ...                    __code__=_Qzan3nwcb3__lambda.__code__.replace(\n'
                      "   ...                               co_name='greet')).items()),\n"
                      '   ...               ),\n'
                      '   ...             _Qzan3nwcb3__lambda)  [-1]\n'
                      '   ...         )())\n'
                      '\n'
                      '   #> (greet-handlers.direct) ; Still the original function object.\n'
                      '   >>> greetQzH_handlers.direct()\n'
                      '   Hello, World!\n'
                      '\n'
                      '   #> (greet-handlers.proxied) ; Proxy does the lookup again.\n'
                      '   >>> greetQzH_handlers.proxied()\n'
                      '   Wassup?\n'),
             __name__='proxyQzHASH_',
             __qualname__='_macro_.proxyQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='proxyQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'sentinelQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda f:
              (
                'hissp.macros.._macro_.let',
                (
                  '_sentinel',
                  (
                    'builtins..object',
                    ),
                  ),
                f,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``sentinel#`` Anaphoric.\n'
                      '\n'
                      'Let ``_sentinel`` be a unique sentinel object in a lexical scope\n'
                      'surrounding ``f``.\n'),
             __name__='sentinelQzHASH_',
             __qualname__='_macro_.sentinelQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='sentinelQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzAT_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda *xs:
             (# when
              (lambda b, c: c()if b else())(
                # ands
                (lambda x0, x1: x0 and x1())(
                  xs,
                  (lambda :
                      __import__('operator').eq(
                        ':*',
                        __import__('operator').itemgetter(
                          (-1))(
                          xs))
                  )),
                (lambda :
                    # throw
                    # hissp.macros.._macro_.throwQzSTAR_
                    (lambda g:g.close()or g.throw)(c for c in'')(
                      SyntaxError(
                        ('trailing :*')))
                )),
              # let
              (
               lambda ixs=iter(
                        xs):
                  (
                    (
                      'lambda',
                      (
                        ':',
                        ':*',
                        'xs',
                        ),
                      '[*xs]',
                      ),
                    ':',
                    *__import__('itertools').chain.from_iterable(
                       map(
                         (lambda X:
                             # ifQzH_else
                             (lambda b, c, a: c()if b else a())(
                               __import__('operator').eq(
                                 X,
                                 (':*')),
                               (lambda :
                                   (
                                     X,
                                     next(
                                       ixs),
                                     )
                               ),
                               (lambda :
                                   (
                                     ':?',
                                     X,
                                     )
                               ))
                         ),
                         ixs)),
                    )
              )())  [-1]
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``@`` 'list of'\n"
                      '\n'
                      'Mnemonic: @rray list.\n'
                      '\n'
                      "Creates the `list` from each expression's result.\n"
                      'A ``:*`` unpacks the next argument:\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (@ :* "AB" (math..sqrt 9) :* "XY" 2 1)\n'
                      '   >>> # QzAT_\n'
                      '   ... (lambda *xs: [*xs])(\n'
                      "   ...   *('AB'),\n"
                      "   ...   __import__('math').sqrt(\n"
                      '   ...     (9)),\n'
                      "   ...   *('XY'),\n"
                      '   ...   (2),\n'
                      '   ...   (1))\n'
                      "   ['A', 'B', 3.0, 'X', 'Y', 2, 1]\n"
                      '\n'
                      'See also:\n'
                      '`# <QzHASH_>`, `% <QzPCENT_>`, `en# <enQzHASH_>`, `operator.matmul`.\n'),
             __name__='QzAT_',
             __qualname__='_macro_.QzAT_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzAT_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda *xs:
             (# when
              (lambda b, c: c()if b else())(
                # ands
                (lambda x0, x1: x0 and x1())(
                  xs,
                  (lambda :
                      __import__('operator').eq(
                        ':*',
                        __import__('operator').itemgetter(
                          (-1))(
                          xs))
                  )),
                (lambda :
                    # throw
                    # hissp.macros.._macro_.throwQzSTAR_
                    (lambda g:g.close()or g.throw)(c for c in'')(
                      SyntaxError(
                        ('trailing :*')))
                )),
              # let
              (
               lambda ixs=iter(
                        xs):
                  (
                    (
                      'lambda',
                      (
                        ':',
                        ':*',
                        'xs',
                        ),
                      '{*xs}',
                      ),
                    ':',
                    *__import__('itertools').chain.from_iterable(
                       map(
                         (lambda X:
                             # ifQzH_else
                             (lambda b, c, a: c()if b else a())(
                               __import__('operator').eq(
                                 X,
                                 (':*')),
                               (lambda :
                                   (
                                     X,
                                     next(
                                       ixs),
                                     )
                               ),
                               (lambda :
                                   (
                                     ':?',
                                     X,
                                     )
                               ))
                         ),
                         ixs)),
                    )
              )())  [-1]
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``#`` 'set of' Mnemonic: Hash (#) set.\n"
                      '\n'
                      "Creates the `set` from each expression's result.\n"
                      'A ``:*`` unpacks the next argument.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (# 1 :* (@ 1 2 3) 4)                    ;Set, with unpacking.\n'
                      '   >>> # QzHASH_\n'
                      '   ... (lambda *xs: {*xs})(\n'
                      '   ...   (1),\n'
                      '   ...   *# QzAT_\n'
                      '   ...    (lambda *xs: [*xs])(\n'
                      '   ...      (1),\n'
                      '   ...      (2),\n'
                      '   ...      (3)),\n'
                      '   ...   (4))\n'
                      '   {1, 2, 3, 4}\n'
                      '\n'
                      'See also: `@ <QzAT_>`, `% <QzPCENT_>`.\n'),
             __name__='QzHASH_',
             __qualname__='_macro_.QzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzPCENT_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda *kvs:
              # cond
              (lambda x0, x1, x2, x3, x4, x5:
                       x1() if x0
                  else x3() if x2()
                  else x5() if x4()
                  else ()
              )(
                __import__('operator').mod(
                  len(
                    kvs),
                  (2)),
                (lambda :
                    # throw
                    # hissp.macros.._macro_.throwQzSTAR_
                    (lambda g:g.close()or g.throw)(c for c in'')(
                      TypeError(
                        ('extra key without value')))
                ),
                (lambda : kvs),
                (lambda :
                    (
                      (
                        'lambda',
                        (
                          *__import__('itertools').starmap(
                             (lambda X, Y: f'x{X}'),
                             filter(
                               (lambda X:
                                   __import__('operator').ne(
                                     ':**',
                                     __import__('operator').itemgetter(
                                       (1))(
                                       X))
                               ),
                               enumerate(
                                 kvs))),
                          ),
                        ('{{{}}}').format(
                          (',').join(
                            __import__('itertools').starmap(
                              (lambda X, Y:
                                  # ifQzH_else
                                  (lambda b, c, a: c()if b else a())(
                                    __import__('operator').eq(
                                      Y,
                                      ':**'),
                                    (lambda : f'**x{X+1}'),
                                    (lambda : f'x{X}:x{X+1}'))
                              ),
                              # QzH_QzGT_
                              __import__('itertools').islice(
                                enumerate(
                                  kvs),
                                (0),
                                None,
                                (2))))),
                        ),
                      *filter(
                         (lambda X:
                             __import__('operator').ne(
                               X,
                               ':**')
                         ),
                         kvs),
                      )
                ),
                (lambda : ':else'),
                (lambda : dict()))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``%`` 'dict of'. Mnemonic: `dict` of pairs (%).\n"
                      '\n'
                      'Key-value pairs are implied by position.\n'
                      'A ``:**`` mapping-unpacks the next argument.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (% 1 2  :** (dict : x 3  y 4)  5 6) ; Dict, with mapping unpacking.\n'
                      '   >>> # QzPCENT_\n'
                      '   ... (lambda x0, x1, x3, x4, x5: {x0:x1,**x3,x4:x5})(\n'
                      '   ...   (1),\n'
                      '   ...   (2),\n'
                      '   ...   dict(\n'
                      '   ...     x=(3),\n'
                      '   ...     y=(4)),\n'
                      '   ...   (5),\n'
                      '   ...   (6))\n'
                      "   {1: 2, 'x': 3, 'y': 4, 5: 6}\n"
                      '\n'
                      '   #> (%)\n'
                      '   >>> # QzPCENT_\n'
                      '   ... {}\n'
                      '   {}\n'
                      '\n'
                      'See also: `@ <QzAT_>`, `# <QzHASH_>`, `operator.mod`.\n'),
             __name__='QzPCENT_',
             __qualname__='_macro_.QzPCENT_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzPCENT_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'prelude',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(
           lambda env=(
                    'builtins..globals',
                    ):
              (
                'builtins..exec',
                (
                  'quote',
                  ('from itertools import *;from operator import *\n'
                   'def engarde(xs,h,f,/,*a,**kw):\n'
                   ' try:return f(*a,**kw)\n'
                   ' except xs as e:return h(e)\n'
                   'def enter(c,f,/,*a):\n'
                   ' with c as C:return f(*a,C)\n'
                   "class Ensue(__import__('collections.abc').abc.Generator):\n"
                   ' send=lambda s,v:s.g.send(v);throw=lambda s,*x:s.g.throw(*x);F=0;X=();Y=[]\n'
                   ' def __init__(s,p):s.p,s.g,s.n=p,s._(s),s.Y\n'
                   ' def _(s,k,v=None):\n'
                   "  while isinstance(s:=k,__class__) and not setattr(s,'sent',v):\n"
                   '   try:k,y=s.p(s),s.Y;v=(yield from y)if s.F or y is s.n else(yield y)\n'
                   '   except s.X as e:v=e\n'
                   '  return k\n'
                   "_macro_=__import__('types').SimpleNamespace()\n"
                   "try: vars(_macro_).update(vars(__import__('hissp')._macro_))\n"
                   'except ModuleNotFoundError: pass'),
                  ),
                env,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("Hissp's bundled micro prelude.\n"
                      '\n'
                      'Brings Hissp up to a minimal standard of usability without adding any\n'
                      'dependencies in the compiled output.\n'
                      '\n'
                      "Mainly intended for single-file scripts that can't have dependencies,\n"
                      'or similarly constrained environments (e.g., embedded,\n'
                      '`readerless mode`). There, the first form should be\n'
                      '``(hissp.._macro_.prelude)``, which is also implied in ``$ lissp -c``\n'
                      'commands. (See the `hissp.prelude` shorthand for Lissp.)\n'
                      '\n'
                      'Larger projects with access to functional and macro libraries need not\n'
                      'use this prelude at all.\n'
                      '\n'
                      'The prelude has several effects:\n'
                      '\n'
                      '* Star imports from `itertools` and `operator`::\n'
                      '\n'
                      '   from itertools import *;from operator import *\n'
                      '\n'
                      '.. _engarde:\n'
                      '\n'
                      '* Defines ``engarde``, which calls a function with exception handler::\n'
                      '\n'
                      '   def engarde(xs,h,f,/,*a,**kw):\n'
                      '    try:return f(*a,**kw)\n'
                      '    except xs as e:return h(e)\n'
                      '\n'
                      '  ``engarde`` with handlers can stack above in a single tuple.\n'
                      '\n'
                      '  See `engarde examples`_ below.\n'
                      '\n'
                      '.. _enter:\n'
                      '\n'
                      '* Defines ``enter``, which calls a function with context manager::\n'
                      '\n'
                      '   def enter(c,f,/,*a):\n'
                      '    with c as C:return f(*a,C)\n'
                      '\n'
                      '  ``enter`` with context managers can stack above in a single tuple.\n'
                      '\n'
                      '  See `enter examples`_ below.\n'
                      '\n'
                      '.. _Ensue:\n'
                      '\n'
                      '* Defines the ``Ensue`` class; trampolined continuation generators::\n'
                      '\n'
                      "   class Ensue(__import__('collections.abc').abc.Generator):\n"
                      '    send=lambda s,v:s.g.send(v);throw=lambda '
                      's,*x:s.g.throw(*x);F=0;X=();Y=[]\n'
                      '    def __init__(s,p):s.p,s.g,s.n=p,s._(s),s.Y\n'
                      '    def _(s,k,v=None):\n'
                      "     while isinstance(s:=k,__class__) and not setattr(s,'sent',v):\n"
                      '      try:k,y=s.p(s),s.Y;v=(yield from y)if s.F or y is s.n else(yield y)\n'
                      '      except s.X as e:v=e\n'
                      '     return k\n'
                      '\n'
                      '  ``Ensue`` takes a step function and returns a generator. The step\n'
                      '  function receives the previous Ensue step and must return the next\n'
                      '  one to continue. Returning a different type raises a `StopIteration`\n'
                      '  with that object. Set the ``Y`` attribute on the current step to\n'
                      '  [Y]ield a value this step. Set the ``F`` attribute to a true value\n'
                      '  to yield values [F]rom the ``Y`` iterable instead. Set the ``X``\n'
                      '  attribute to an e[X]ception class or tuple to catch any targeted\n'
                      '  exceptions on the next step. Each step keeps a ``sent`` attribute,\n'
                      '  which is the value sent to the generator this step, or the exception\n'
                      '  caught this step instead.\n'
                      '\n'
                      '  See `Ensue examples`_ and `enter examples`_ below.\n'
                      '\n'
                      '  See also: `types.coroutine`, `collections.abc.Generator`,\n'
                      '  `loop-from <loopQzH_from>`.\n'
                      '\n'
                      '* Adds the bundled macros, but only if available\n'
                      '  (macros are typically only used at compile time),\n'
                      '  so its compiled expansion does not require Hissp to be installed.\n'
                      '  (This replaces ``_macro_`` if you already had one.)::\n'
                      '\n'
                      "   _macro_=__import__('types').SimpleNamespace()\n"
                      "   try: vars(_macro_).update(vars(__import__('hissp')._macro_))\n"
                      '   except ModuleNotFoundError: pass\n'
                      '\n'
                      'Prelude Usage\n'
                      '=============\n'
                      'The `REPL` has the bundled macros loaded by default,\n'
                      'but not the prelude. Invoke ``(prelude)`` to get the rest.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (prelude)\n'
                      '   >>> # prelude\n'
                      "   ... __import__('builtins').exec(\n"
                      "   ...   ('from itertools import *;from operator import *\\n'\n"
                      "   ...    'def engarde(xs,h,f,/,*a,**kw):\\n'\n"
                      "   ...    ' try:return f(*a,**kw)\\n'\n"
                      "   ...    ' except xs as e:return h(e)\\n'\n"
                      "   ...    'def enter(c,f,/,*a):\\n'\n"
                      "   ...    ' with c as C:return f(*a,C)\\n'\n"
                      '   ...    "class Ensue(__import__(\'collections.abc\').abc.Generator):\\n"\n'
                      "   ...    ' send=lambda s,v:s.g.send(v);throw=lambda "
                      "s,*x:s.g.throw(*x);F=0;X=();Y=[]\\n'\n"
                      "   ...    ' def __init__(s,p):s.p,s.g,s.n=p,s._(s),s.Y\\n'\n"
                      "   ...    ' def _(s,k,v=None):\\n'\n"
                      '   ...    "  while isinstance(s:=k,__class__) and not '
                      'setattr(s,\'sent\',v):\\n"\n'
                      "   ...    '   try:k,y=s.p(s),s.Y;v=(yield from y)if s.F or y is s.n "
                      "else(yield y)\\n'\n"
                      "   ...    '   except s.X as e:v=e\\n'\n"
                      "   ...    '  return k\\n'\n"
                      '   ...    "_macro_=__import__(\'types\').SimpleNamespace()\\n"\n'
                      '   ...    "try: '
                      'vars(_macro_).update(vars(__import__(\'hissp\')._macro_))\\n"\n'
                      "   ...    'except ModuleNotFoundError: pass'),\n"
                      "   ...   __import__('builtins').globals())\n"
                      '\n'
                      'See also, `alias`.\n'
                      '\n'
                      'engarde examples\n'
                      '----------------\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (engarde `(,FloatingPointError ,ZeroDivisionError) ;two targets\n'
                      '   #..         (lambda e (print "Oops!") e)   ;handler (returns exception)\n'
                      '   #..         truediv 6 0)                   ;calls it on your behalf\n'
                      '   >>> engarde(\n'
                      '   ...   (\n'
                      '   ...     FloatingPointError,\n'
                      '   ...     ZeroDivisionError,\n'
                      '   ...     ),\n'
                      '   ...   (lambda e:\n'
                      '   ...      (print(\n'
                      "   ...         ('Oops!')),\n"
                      '   ...       e)  [-1]\n'
                      '   ...   ),\n'
                      '   ...   truediv,\n'
                      '   ...   (6),\n'
                      '   ...   (0))\n'
                      '   Oops!\n'
                      "   ZeroDivisionError('division by zero')\n"
                      '\n'
                      '   #> (engarde ArithmeticError repr truediv 6 0) ;superclass target\n'
                      '   >>> engarde(\n'
                      '   ...   ArithmeticError,\n'
                      '   ...   repr,\n'
                      '   ...   truediv,\n'
                      '   ...   (6),\n'
                      '   ...   (0))\n'
                      '   "ZeroDivisionError(\'division by zero\')"\n'
                      '\n'
                      '   #> (engarde ArithmeticError repr truediv 6 2) ;returned answer\n'
                      '   >>> engarde(\n'
                      '   ...   ArithmeticError,\n'
                      '   ...   repr,\n'
                      '   ...   truediv,\n'
                      '   ...   (6),\n'
                      '   ...   (2))\n'
                      '   3.0\n'
                      '\n'
                      '   #> (engarde Exception                      ;The stacked outer engarde\n'
                      '   #.. print\n'
                      '   #.. engarde ZeroDivisionError              ; calls the inner.\n'
                      '   #.. (lambda e (print "It means what you want it to mean."))\n'
                      '   #.. truediv "6" 0)                         ;Try variations.\n'
                      '   >>> engarde(\n'
                      '   ...   Exception,\n'
                      '   ...   print,\n'
                      '   ...   engarde,\n'
                      '   ...   ZeroDivisionError,\n'
                      '   ...   (lambda e:\n'
                      '   ...       print(\n'
                      "   ...         ('It means what you want it to mean.'))\n"
                      '   ...   ),\n'
                      '   ...   truediv,\n'
                      "   ...   ('6'),\n"
                      '   ...   (0))\n'
                      "   unsupported operand type(s) for /: 'str' and 'int'\n"
                      '\n'
                      '   #> (engarde Exception\n'
                      '   #..         (lambda x x.__cause__)\n'
                      '   #..         (lambda : (throw-from Exception (Exception "msg"))))\n'
                      '   >>> engarde(\n'
                      '   ...   Exception,\n'
                      '   ...   (lambda x: x.__cause__),\n'
                      '   ...   (lambda :\n'
                      '   ...       # throwQzH_from\n'
                      '   ...       # hissp.macros.._macro_.throwQzSTAR_\n'
                      "   ...       (lambda g:g.close()or g.throw)(c for c in'')(\n"
                      '   ...         # hissp.macros.._macro_.let\n'
                      '   ...         (\n'
                      '   ...          lambda _Qzzkusd5eu__G=(lambda _Qzzkusd5eu__x:\n'
                      '   ...                     # hissp.macros.._macro_.ifQzH_else\n'
                      '   ...                     (lambda b, c, a: c()if b else a())(\n'
                      "   ...                       __import__('builtins').isinstance(\n"
                      '   ...                         _Qzzkusd5eu__x,\n'
                      "   ...                         __import__('builtins').BaseException),\n"
                      '   ...                       (lambda : _Qzzkusd5eu__x),\n'
                      '   ...                       (lambda : _Qzzkusd5eu__x()))\n'
                      '   ...                 ):\n'
                      '   ...             # hissp.macros.._macro_.attach\n'
                      '   ...             # hissp.macros.._macro_.let\n'
                      '   ...             (\n'
                      '   ...              lambda _Qzwawunnb6__target=_Qzzkusd5eu__G(\n'
                      '   ...                       Exception):\n'
                      "   ...                (__import__('builtins').setattr(\n"
                      '   ...                   _Qzwawunnb6__target,\n'
                      "   ...                   '__cause__',\n"
                      '   ...                   _Qzzkusd5eu__G(\n'
                      '   ...                     Exception(\n'
                      "   ...                       ('msg')))),\n"
                      '   ...                 _Qzwawunnb6__target)  [-1]\n'
                      '   ...             )()\n'
                      '   ...         )())\n'
                      '   ...   ))\n'
                      "   Exception('msg')\n"
                      '\n'
                      'Ensue examples\n'
                      '--------------\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (.update (globals)\n'
                      '   #..  : fibonacci\n'
                      '   #..  (lambda (: a 1  b 1)\n'
                      '   #..    (Ensue (lambda (step)\n'
                      "   #..             (setattr step 'Y a)        ;Y for yield.\n"
                      '   #..             (fibonacci b (add a b))))))\n'
                      '   >>> globals().update(\n'
                      '   ...   fibonacci=(\n'
                      '   ...              lambda a=(1),\n'
                      '   ...                     b=(1):\n'
                      '   ...                 Ensue(\n'
                      '   ...                   (lambda step:\n'
                      '   ...                      (setattr(\n'
                      '   ...                         step,\n'
                      "   ...                         'Y',\n"
                      '   ...                         a),\n'
                      '   ...                       fibonacci(\n'
                      '   ...                         b,\n'
                      '   ...                         add(\n'
                      '   ...                           a,\n'
                      '   ...                           b)))  [-1]\n'
                      '   ...                   ))\n'
                      '   ...             ))\n'
                      '\n'
                      '   #> (list (islice (fibonacci) 7))\n'
                      '   >>> list(\n'
                      '   ...   islice(\n'
                      '   ...     fibonacci(),\n'
                      '   ...     (7)))\n'
                      '   [1, 1, 2, 3, 5, 8, 13]\n'
                      '\n'
                      '   #> (.update (globals) ; Terminate by not returning an Ensue.\n'
                      '   #..  : my-range\n'
                      '   #..  (lambda in\n'
                      '   #..    (Ensue (lambda (step)\n'
                      '   #..             (when (lt i n)             ;Acts like a while loop.\n'
                      "   #..               (setattr step 'Y i)\n"
                      '   #..               (my-range (add i 1) n)))))) ;Conditional recursion.\n'
                      '   #..\n'
                      '   >>> globals().update(\n'
                      '   ...   myQzH_range=(lambda i, n:\n'
                      '   ...                   Ensue(\n'
                      '   ...                     (lambda step:\n'
                      '   ...                         # when\n'
                      '   ...                         (lambda b, c: c()if b else())(\n'
                      '   ...                           lt(\n'
                      '   ...                             i,\n'
                      '   ...                             n),\n'
                      '   ...                           (lambda :\n'
                      '   ...                              (setattr(\n'
                      '   ...                                 step,\n'
                      "   ...                                 'Y',\n"
                      '   ...                                 i),\n'
                      '   ...                               myQzH_range(\n'
                      '   ...                                 add(\n'
                      '   ...                                   i,\n'
                      '   ...                                   (1)),\n'
                      '   ...                                 n))  [-1]\n'
                      '   ...                           ))\n'
                      '   ...                     ))\n'
                      '   ...               ))\n'
                      '\n'
                      '   #> (list (my-range 1 6))\n'
                      '   >>> list(\n'
                      '   ...   myQzH_range(\n'
                      '   ...     (1),\n'
                      '   ...     (6)))\n'
                      '   [1, 2, 3, 4, 5]\n'
                      '\n'
                      '   #> (Ensue (lambda (step)\n'
                      '   #..         (attach step :\n'
                      '   #..           F True ; Set F for yield-From mode.\n'
                      "   #..           Y '(1 2 3 4 5))\n"
                      '   #..         None))\n'
                      '   >>> Ensue(\n'
                      '   ...   (lambda step:\n'
                      '   ...      (# attach\n'
                      '   ...       # hissp.macros.._macro_.let\n'
                      '   ...       (lambda _Qzwg5wn73w__target=step:\n'
                      "   ...          (__import__('builtins').setattr(\n"
                      '   ...             _Qzwg5wn73w__target,\n'
                      "   ...             'F',\n"
                      '   ...             True),\n'
                      "   ...           __import__('builtins').setattr(\n"
                      '   ...             _Qzwg5wn73w__target,\n'
                      "   ...             'Y',\n"
                      '   ...             ((1),\n'
                      '   ...              (2),\n'
                      '   ...              (3),\n'
                      '   ...              (4),\n'
                      '   ...              (5),)),\n'
                      '   ...           _Qzwg5wn73w__target)  [-1]\n'
                      '   ...       )(),\n'
                      '   ...       None)  [-1]\n'
                      '   ...   ))\n'
                      '   <...Ensue object at ...>\n'
                      '\n'
                      '   #> (list _)\n'
                      '   >>> list(\n'
                      '   ...   _)\n'
                      '   [1, 2, 3, 4, 5]\n'
                      '\n'
                      '   #> (define recycle\n'
                      '   #..  (lambda (itr)\n'
                      '   #..    (Ensue (lambda (step)\n'
                      '   #..             ;; Implicit continuation; step is an Ensue.\n'
                      '   #..             (attach step : Y itr  F 1)))))\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   recycle=(lambda itr:\n'
                      '   ...               Ensue(\n'
                      '   ...                 (lambda step:\n'
                      '   ...                     # attach\n'
                      '   ...                     # hissp.macros.._macro_.let\n'
                      '   ...                     (lambda _Qzwg5wn73w__target=step:\n'
                      "   ...                        (__import__('builtins').setattr(\n"
                      '   ...                           _Qzwg5wn73w__target,\n'
                      "   ...                           'Y',\n"
                      '   ...                           itr),\n'
                      "   ...                         __import__('builtins').setattr(\n"
                      '   ...                           _Qzwg5wn73w__target,\n'
                      "   ...                           'F',\n"
                      '   ...                           (1)),\n'
                      '   ...                         _Qzwg5wn73w__target)  [-1]\n'
                      '   ...                     )()\n'
                      '   ...                 ))\n'
                      '   ...           ))\n'
                      '\n'
                      "   #> (-> '(1 2 3) recycle (islice 7) list)\n"
                      '   >>> # QzH_QzGT_\n'
                      '   ... list(\n'
                      '   ...   islice(\n'
                      '   ...     recycle(\n'
                      '   ...       ((1),\n'
                      '   ...        (2),\n'
                      '   ...        (3),)),\n'
                      '   ...     (7)))\n'
                      '   [1, 2, 3, 1, 2, 3, 1]\n'
                      '\n'
                      '   #> (.update (globals)\n'
                      '   #..  : echo\n'
                      '   #..  (Ensue (lambda (step)\n'
                      "   #..           (setattr step 'Y step.sent)\n"
                      '   #..           step)))\n'
                      '   >>> globals().update(\n'
                      '   ...   echo=Ensue(\n'
                      '   ...          (lambda step:\n'
                      '   ...             (setattr(\n'
                      '   ...                step,\n'
                      "   ...                'Y',\n"
                      '   ...                step.sent),\n'
                      '   ...              step)  [-1]\n'
                      '   ...          )))\n'
                      '\n'
                      '   #> (.send echo None) ; Always send a None first. Same as Python.\n'
                      '   >>> echo.send(\n'
                      '   ...   None)\n'
                      '\n'
                      '   #> (.send echo "Yodel!") ; Generators are two-way.\n'
                      '   >>> echo.send(\n'
                      "   ...   ('Yodel!'))\n"
                      "   'Yodel!'\n"
                      '\n'
                      '   #> (.send echo 42)\n'
                      '   >>> echo.send(\n'
                      '   ...   (42))\n'
                      '   42\n'
                      '\n'
                      'enter examples\n'
                      '--------------\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> :@##contextlib..contextmanager\n'
                      '   #..(defun wrap (msg)\n'
                      '   #..  (print "enter" msg)\n'
                      '   #..  (Ensue (lambda (step)\n'
                      "   #..           (setattr step 'Y msg)\n"
                      '   #..           (Ensue (lambda (step)\n'
                      '   #..                    (print "exit" msg))))))\n'
                      '   >>> # hissp.macros.._macro_.define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   wrap=# hissp.macros.._macro_.progn\n'
                      '   ...        (# defun\n'
                      '   ...         # hissp.macros.._macro_.define\n'
                      "   ...         __import__('builtins').globals().update(\n"
                      '   ...           wrap=# hissp.macros.._macro_.fun\n'
                      '   ...                # hissp.macros.._macro_.let\n'
                      '   ...                (\n'
                      '   ...                 lambda _Qztl624wbs__lambda=(lambda msg:\n'
                      '   ...                           (print(\n'
                      "   ...                              ('enter'),\n"
                      '   ...                              msg),\n'
                      '   ...                            Ensue(\n'
                      '   ...                              (lambda step:\n'
                      '   ...                                 (setattr(\n'
                      '   ...                                    step,\n'
                      "   ...                                    'Y',\n"
                      '   ...                                    msg),\n'
                      '   ...                                  Ensue(\n'
                      '   ...                                    (lambda step:\n'
                      '   ...                                        print(\n'
                      "   ...                                          ('exit'),\n"
                      '   ...                                          msg)\n'
                      '   ...                                    )))  [-1]\n'
                      '   ...                              )))  [-1]\n'
                      '   ...                        ):\n'
                      '   ...                   ((\n'
                      "   ...                      *__import__('itertools').starmap(\n"
                      '   ...                         _Qztl624wbs__lambda.__setattr__,\n'
                      "   ...                         __import__('builtins').dict(\n"
                      "   ...                           __name__='wrap',\n"
                      "   ...                           __qualname__='wrap',\n"
                      '   ...                           '
                      '__code__=_Qztl624wbs__lambda.__code__.replace(\n'
                      "   ...                                      co_name='wrap')).items()),\n"
                      '   ...                      ),\n'
                      '   ...                    _Qztl624wbs__lambda)  [-1]\n'
                      '   ...                )()),\n'
                      "   ...         __import__('contextlib').contextmanager(\n"
                      '   ...           wrap))  [-1])\n'
                      '\n'
                      "   #> (enter (wrap 'A)\n"
                      '   #..       (lambda a (print a)))\n'
                      '   >>> enter(\n'
                      '   ...   wrap(\n'
                      "   ...     'A'),\n"
                      '   ...   (lambda a:\n'
                      '   ...       print(\n'
                      '   ...         a)\n'
                      '   ...   ))\n'
                      '   enter A\n'
                      '   A\n'
                      '   exit A\n'
                      '\n'
                      "   #> (enter (wrap 'A)\n"
                      "   #.. enter (wrap 'B)\n"
                      "   #.. enter (wrap 'C) ; You can stack them.\n"
                      '   #.. (lambda abc (print a b c)))\n'
                      '   >>> enter(\n'
                      '   ...   wrap(\n'
                      "   ...     'A'),\n"
                      '   ...   enter,\n'
                      '   ...   wrap(\n'
                      "   ...     'B'),\n"
                      '   ...   enter,\n'
                      '   ...   wrap(\n'
                      "   ...     'C'),\n"
                      '   ...   (lambda a, b, c:\n'
                      '   ...       print(\n'
                      '   ...         a,\n'
                      '   ...         b,\n'
                      '   ...         c)\n'
                      '   ...   ))\n'
                      '   enter A\n'
                      '   enter B\n'
                      '   enter C\n'
                      '   A B C\n'
                      '   exit C\n'
                      '   exit B\n'
                      '   exit A\n'
                      '\n'
                      '   #> (define suppress-zde\n'
                      '   #..  (contextlib..contextmanager\n'
                      '   #..   (lambda :\n'
                      '   #..     (Ensue (lambda (step)\n'
                      '   #..              (attach step :\n'
                      '   #..                Y None\n'
                      '   #..                X ZeroDivisionError) ; X for eXcept (can be a tuple).\n'
                      '   #..              (Ensue (lambda (step)\n'
                      '   #..                       (print "Caught a" step.sent))))))))\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      "   ...   suppressQzH_zde=__import__('contextlib').contextmanager(\n"
                      '   ...                     (lambda :\n'
                      '   ...                         Ensue(\n'
                      '   ...                           (lambda step:\n'
                      '   ...                              (# attach\n'
                      '   ...                               # hissp.macros.._macro_.let\n'
                      '   ...                               (lambda _Qzwg5wn73w__target=step:\n'
                      "   ...                                  (__import__('builtins').setattr(\n"
                      '   ...                                     _Qzwg5wn73w__target,\n'
                      "   ...                                     'Y',\n"
                      '   ...                                     None),\n'
                      "   ...                                   __import__('builtins').setattr(\n"
                      '   ...                                     _Qzwg5wn73w__target,\n'
                      "   ...                                     'X',\n"
                      '   ...                                     ZeroDivisionError),\n'
                      '   ...                                   _Qzwg5wn73w__target)  [-1]\n'
                      '   ...                               )(),\n'
                      '   ...                               Ensue(\n'
                      '   ...                                 (lambda step:\n'
                      '   ...                                     print(\n'
                      "   ...                                       ('Caught a'),\n"
                      '   ...                                       step.sent)\n'
                      '   ...                                 )))  [-1]\n'
                      '   ...                           ))\n'
                      '   ...                     )))\n'
                      '\n'
                      '   #> (enter (suppress-zde)\n'
                      '   #..  (lambda _ (truediv 1 0)))\n'
                      '   >>> enter(\n'
                      '   ...   suppressQzH_zde(),\n'
                      '   ...   (lambda _:\n'
                      '   ...       truediv(\n'
                      '   ...         (1),\n'
                      '   ...         (0))\n'
                      '   ...   ))\n'
                      '   Caught a division by zero\n'
                      '\n'
                      '   #> (enter (suppress-zde) ; No exception, so step.sent was .send() value.\n'
                      '   #..  (lambda _ (truediv 4 2)))\n'
                      '   >>> enter(\n'
                      '   ...   suppressQzH_zde(),\n'
                      '   ...   (lambda _:\n'
                      '   ...       truediv(\n'
                      '   ...         (4),\n'
                      '   ...         (2))\n'
                      '   ...   ))\n'
                      '   Caught a None\n'
                      '   2.0\n'
                      '\n'
                      '   #> (enter (suppress-zde)\n'
                      '   #..  (lambda _ (throw Exception)))\n'
                      '   >>> enter(\n'
                      '   ...   suppressQzH_zde(),\n'
                      '   ...   (lambda _:\n'
                      '   ...       # throw\n'
                      '   ...       # hissp.macros.._macro_.throwQzSTAR_\n'
                      "   ...       (lambda g:g.close()or g.throw)(c for c in'')(\n"
                      '   ...         Exception)\n'
                      '   ...   ))\n'
                      '   Traceback (most recent call last):\n'
                      '     ...\n'
                      '   Exception\n'),
             __name__='prelude',
             __qualname__='_macro_.prelude',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='prelude')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'import',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda *args:
              (
                'builtins..print',
                (
                  'codecs..encode',
                  (
                    'hissp.macros..QzMaybe_._TAO',
                    'inspect..getsource',
                    ),
                  (
                    'quote',
                    'rot13',
                    ),
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __name__='import',
             __qualname__='_macro_.import',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='import')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'mix',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda *args:
              ('').join(
                map(
                  __import__('hissp').readerless,
                  args))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Injection. Compiles each arg to Python and concatenates the fragments.\n'
                      '\n'
                      'Lissp features like munging and fully-qualified identifiers can be\n'
                      'freely mixed with Python expressions like slicing, infix operators\n'
                      'and list comprehensions by using `fragment token`\\ s:\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (mix |[|%|+|(.lower %)| for |%| in |string..ascii_uppercase|[:10]]|)\n'
                      '   >>> # mix\n'
                      '   ... [QzPCENT_+QzPCENT_.lower() for QzPCENT_ in '
                      "__import__('string').ascii_uppercase[:10]]\n"
                      "   ['Aa', 'Bb', 'Cc', 'Dd', 'Ee', 'Ff', 'Gg', 'Hh', 'Ii', 'Jj']\n"
                      '\n'
                      'Beware that a `str atom` like ``|:|`` is still a `control word`,\n'
                      'and like ``|foo.|`` is still a `module handle`, even when made with\n'
                      'a `fragment token`. However, Python allows whitespace in many areas\n'
                      'where it is not conventional to do so, making fragments like\n'
                      '``| :|`` or ``|foo .|`` viable workarounds in such cases.\n'),
             __name__='mix',
             __qualname__='_macro_.mix',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='mix')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# hissp.macros.._macro_.let
(lambda _sentinel=__import__('builtins').object():
    # defmacro
    __import__('builtins').setattr(
      __import__('builtins').globals().get(
        ('_macro_')),
      'defvar',
      # hissp.macros.._macro_.fun
      # hissp.macros.._macro_.let
      (
       lambda _Qzwfz72h4o__lambda=(
               lambda name,
                      default=_sentinel:
                  (
                    'hissp.macros.._macro_.unless',
                    (
                      'operator..contains',
                      (
                        'builtins..globals',
                        ),
                      (
                        'quote',
                        name,
                        ),
                      ),
                    (
                      'hissp.macros.._macro_.define',
                      name,
                      (
                        'contextvars..ContextVar',
                        (
                          'quote',
                          __import__('hissp').demunge(
                            name),
                          ),
                        ':',
                        *# unless
                         (lambda b, a: ()if b else a())(
                           __import__('operator').is_(
                             default,
                             _sentinel),
                           (lambda :
                               (
                                 'hissp.macros..QzMaybe_.default',
                                 default,
                                 )
                           )),
                        ),
                      ),
                    )
              ):
         ((
            *__import__('itertools').starmap(
               _Qzwfz72h4o__lambda.__setattr__,
               __import__('builtins').dict(
                 __doc__=('Creates a `contextvars.ContextVar`, unless it exists.\n'
                          '\n'
                          'The default is optional, but cannot be altered once set, however, a\n'
                          'new binding may be set for a `contextvars.Context`.\n'
                          '\n'
                          'Intended for use at the top level only, because Python currently\n'
                          'has no way of deleting a ``ContextVar`` once it has been added to\n'
                          'the current ``Context``. (Although a ``ContextVar`` could be\n'
                          'deleted from the globals and replaced with a new one with the same\n'
                          'name and a different default value, the old ``ContextVar`` will\n'
                          'also be in the ``Context``.)\n'
                          '\n'
                          'See `binding` for usage examples.\n'
                          '\n'
                          'See also: `defonce`.'),
                 __name__='defvar',
                 __qualname__='_macro_.defvar',
                 __code__=_Qzwfz72h4o__lambda.__code__.replace(
                            co_name='defvar')).items()),
            ),
          _Qzwfz72h4o__lambda)  [-1]
      )())
)()

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'binding',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda pairs, *body:
              (
                '.run',
                (
                  'contextvars..copy_context',
                  ),
                (
                  'lambda',
                  ':',
                  *__import__('itertools').starmap(
                     (lambda k, v:
                         (
                           '.set',
                           k,
                           v,
                           )
                     ),
                     (lambda X:
                         zip(
                           X,
                           X,
                           strict=True)
                     )(
                       iter(
                         pairs))),
                  *body,
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Runs body in a new `contextvars.Context`, with additional bindings.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (defvar *greeting*)\n'
                      '   >>> # defvar\n'
                      '   ... # hissp.macros.._macro_.unless\n'
                      '   ... (lambda b, a: ()if b else a())(\n'
                      "   ...   __import__('operator').contains(\n"
                      "   ...     __import__('builtins').globals(),\n"
                      "   ...     'QzSTAR_greetingQzSTAR_'),\n"
                      '   ...   (lambda :\n'
                      '   ...       # hissp.macros.._macro_.define\n'
                      "   ...       __import__('builtins').globals().update(\n"
                      "   ...         QzSTAR_greetingQzSTAR_=__import__('contextvars').ContextVar(\n"
                      "   ...                                  '*greeting*'))\n"
                      '   ...   ))\n'
                      '\n'
                      '   #> *greeting*\n'
                      '   >>> QzSTAR_greetingQzSTAR_\n'
                      "   <ContextVar name='*greeting*' at 0x...>\n"
                      '\n'
                      '   #> (defvar *greeted* "World!")\n'
                      '   >>> # defvar\n'
                      '   ... # hissp.macros.._macro_.unless\n'
                      '   ... (lambda b, a: ()if b else a())(\n'
                      "   ...   __import__('operator').contains(\n"
                      "   ...     __import__('builtins').globals(),\n"
                      "   ...     'QzSTAR_greetedQzSTAR_'),\n"
                      '   ...   (lambda :\n'
                      '   ...       # hissp.macros.._macro_.define\n'
                      "   ...       __import__('builtins').globals().update(\n"
                      "   ...         QzSTAR_greetedQzSTAR_=__import__('contextvars').ContextVar(\n"
                      "   ...                                 '*greeted*',\n"
                      "   ...                                 default=('World!')))\n"
                      '   ...   ))\n'
                      '\n'
                      '   #> *greeted*\n'
                      '   >>> QzSTAR_greetedQzSTAR_\n'
                      "   <ContextVar name='*greeted*' default='World!' at 0x...>\n"
                      '\n'
                      '   #> (defun greet : (print (.get *greeting* "Hello,") (.get *greeted*)))\n'
                      '   >>> # defun\n'
                      '   ... # hissp.macros.._macro_.define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   greet=# hissp.macros.._macro_.fun\n'
                      '   ...         # hissp.macros.._macro_.let\n'
                      '   ...         (\n'
                      '   ...          lambda _Qzan3nwcb3__lambda=(lambda :\n'
                      '   ...                     print(\n'
                      '   ...                       QzSTAR_greetingQzSTAR_.get(\n'
                      "   ...                         ('Hello,')),\n"
                      '   ...                       QzSTAR_greetedQzSTAR_.get())\n'
                      '   ...                 ):\n'
                      '   ...            ((\n'
                      "   ...               *__import__('itertools').starmap(\n"
                      '   ...                  _Qzan3nwcb3__lambda.__setattr__,\n'
                      "   ...                  __import__('builtins').dict(\n"
                      "   ...                    __name__='greet',\n"
                      "   ...                    __qualname__='greet',\n"
                      '   ...                    __code__=_Qzan3nwcb3__lambda.__code__.replace(\n'
                      "   ...                               co_name='greet')).items()),\n"
                      '   ...               ),\n'
                      '   ...             _Qzan3nwcb3__lambda)  [-1]\n'
                      '   ...         )())\n'
                      '\n'
                      '   #> (greet)\n'
                      '   >>> greet()\n'
                      '   Hello, World!\n'
                      '\n'
                      '   #> (binding (*greeting* "Goodbye,"\n'
                      '   #..          *greeted* "all!")\n'
                      '   #..  (greet))\n'
                      '   >>> # binding\n'
                      "   ... __import__('contextvars').copy_context().run(\n"
                      '   ...   (lambda :\n'
                      '   ...      (QzSTAR_greetingQzSTAR_.set(\n'
                      "   ...         ('Goodbye,')),\n"
                      '   ...       QzSTAR_greetedQzSTAR_.set(\n'
                      "   ...         ('all!')),\n"
                      '   ...       greet())  [-1]\n'
                      '   ...   ))\n'
                      '   Goodbye, all!\n'
                      '\n'
                      '   #> (greet)\n'
                      '   >>> greet()\n'
                      '   Hello, World!\n'
                      '\n'
                      'See also: `defvar`.\n'),
             __name__='binding',
             __qualname__='_macro_.binding',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='binding')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'myQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(
           lambda targets_or_scope,
                  expr=None,
                  scope=(),
                  **kwargs:
              # let
              (lambda ns=__import__('types').SimpleNamespace():
                 (setattr(
                    ns,
                    'form',
                    (lambda X:
                        # cond
                        (lambda x0, x1, x2, x3, x4, x5:
                                 x1() if x0
                            else x3() if x2()
                            else x5() if x4()
                            else ()
                        )(
                          isinstance(
                            X,
                            __import__('hissp').reader.Kwarg),
                          (lambda :
                              (
                                'hissp.macros.._macro_.setQzAT_',
                                __import__('hissp').munge(
                                  f"my.{X.k}"),
                                X.v,
                                )
                          ),
                          (lambda :
                              __import__('hissp').is_node(
                                X)
                          ),
                          (lambda :
                              (
                                *map(
                                   ns.form,
                                   X),
                                )
                          ),
                          (lambda : ':else'),
                          (lambda : X))
                    )),
                  # ifQzH_else
                  (lambda b, c, a: c()if b else a())(
                    expr is None and scope == (),
                    (lambda :
                        (
                          'hissp.macros.._macro_.let',
                          (
                            'my',
                            (
                              'types..SimpleNamespace',
                              ':',
                              *__import__('itertools').chain.from_iterable(
                                 kwargs.items()),
                              ),
                            ),
                          ns.form(
                            targets_or_scope),
                          )
                    ),
                    (lambda :
                        (
                          'hissp.macros.._macro_.let',
                          (
                            'my',
                            (
                              'types..SimpleNamespace',
                              ':',
                              ':**',
                              (
                                'hissp.macros.._macro_.let',
                                (
                                  '_Qzbvloekbs__expr',
                                  expr,
                                  ),
                                ('[{}()\n for ({})\n in [{}]]  [0]').format(
                                  __import__('hissp').readerless(
                                    'builtins..locals'),
                                  __import__('hissp').demunge(
                                    targets_or_scope),
                                  '_Qzbvloekbs__expr'),
                                ),
                              *__import__('itertools').chain.from_iterable(
                                 kwargs.items()),
                              ),
                            ),
                          (
                            'my.__dict__.pop',
                            (
                              'quote',
                              '_Qzbvloekbs__expr',
                              ),
                            None,
                            ),
                          (
                            'my.__dict__.pop',
                            "('.0')",
                            None,
                            ),
                          ns.form(
                            scope),
                          )
                    )))  [-1]
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``my#`` Anaphoric. Injection. `let` ``my`` be a fresh\n'
                      '`types.SimpleNamespace` in a lexical scope.\n'
                      '\n'
                      'Creates a local namespace for imperative-style (re)assignments.\n'
                      '`Kwarg token`\\ s in scope translate to `set@ <setQzAT_>`.\n'
                      '\n'
                      'Often combined with branching macros to reuse the results of an\n'
                      "expression, with uses similar to Python's 'walrus' operator ``:=``.\n"
                      'See `python-grammar:assignment_expression`.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> my#(print x=(op#add 1 1) my.x)\n'
                      '   >>> # hissp.macros.._macro_.let\n'
                      "   ... (lambda my=__import__('types').SimpleNamespace():\n"
                      '   ...     print(\n'
                      '   ...       # hissp.macros.._macro_.setQzAT_\n'
                      '   ...       # hissp.macros.._macro_.let\n'
                      '   ...       (\n'
                      "   ...        lambda _Qzwk5j5q64__value=__import__('operator').add(\n"
                      '   ...                 (1),\n'
                      '   ...                 (1)):\n'
                      '   ...          (# hissp.macros.._macro_.define\n'
                      "   ...           __import__('builtins').setattr(\n"
                      '   ...             my,\n'
                      "   ...             'x',\n"
                      '   ...             _Qzwk5j5q64__value),\n'
                      '   ...           _Qzwk5j5q64__value)  [-1]\n'
                      '   ...       )(),\n'
                      '   ...       my.x)\n'
                      '   ... )()\n'
                      '   2 2\n'
                      '\n'
                      '   #> my#my ; Empty namespace shorthand.\n'
                      '   >>> # hissp.macros.._macro_.let\n'
                      "   ... (lambda my=__import__('types').SimpleNamespace(): my)()\n"
                      '   namespace()\n'
                      '\n'
                      '   #> my##foo=2 my ; Initial content from read-time kwarg.\n'
                      '   >>> # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      "   ...  lambda my=__import__('types').SimpleNamespace(\n"
                      '   ...           foo=(2)):\n'
                      '   ...     my)()\n'
                      '   namespace(foo=2)\n'
                      '\n'
                      '   #> my##outer=2 my###inner=1 bridge=my (@ my.bridge.outer my.inner)\n'
                      '   >>> # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      "   ...  lambda my=__import__('types').SimpleNamespace(\n"
                      '   ...           outer=(2)):\n'
                      '   ...     # hissp.macros.._macro_.let\n'
                      '   ...     (\n'
                      "   ...      lambda my=__import__('types').SimpleNamespace(\n"
                      '   ...               inner=(1),\n'
                      '   ...               bridge=my):\n'
                      '   ...         # QzAT_\n'
                      '   ...         (lambda *xs: [*xs])(\n'
                      '   ...           my.bridge.outer,\n'
                      '   ...           my.inner)\n'
                      '   ...     )()\n'
                      '   ... )()\n'
                      '   [2, 1]\n'
                      '\n'
                      'With at least two positional arguments, the first is an injected\n'
                      'Python assignment target, and the second its value:\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> my### a,b,[c,*xs] '(1 2 |spam|) my ; Nested unpacking.\n"
                      '   >>> # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      "   ...  lambda my=__import__('types').SimpleNamespace(\n"
                      '   ...           **# hissp.macros.._macro_.let\n'
                      '   ...             (\n'
                      '   ...              lambda _Qze4jatheu__expr=((1),\n'
                      '   ...                      (2),\n'
                      "   ...                      'spam',):\n"
                      "   ...                 [__import__('builtins').locals()\n"
                      '   ...                  for (a,b,[c,*xs])\n'
                      '   ...                  in [_Qze4jatheu__expr]]  [0]\n'
                      '   ...             )()):\n'
                      '   ...    (my.__dict__.pop(\n'
                      "   ...       '_Qze4jatheu__expr',\n"
                      '   ...       None),\n'
                      '   ...     my.__dict__.pop(\n'
                      "   ...       ('.0'),\n"
                      '   ...       None),\n'
                      '   ...     my)  [-1]\n'
                      '   ... )()\n'
                      "   namespace(a=1, b=2, c='s', xs=['p', 'a', 'm'])\n"
                      '\n'
                      'Use `zap@ <zapQzAT_>` for augmented assignments:\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> my###a,b 'AB (@ (zap@ my.a iadd c='C) my)\n"
                      '   >>> # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      "   ...  lambda my=__import__('types').SimpleNamespace(\n"
                      '   ...           **# hissp.macros.._macro_.let\n'
                      "   ...             (lambda _Qzec6padpw__expr='AB':\n"
                      "   ...                 [__import__('builtins').locals()\n"
                      '   ...                  for (a,b)\n'
                      '   ...                  in [_Qzec6padpw__expr]]  [0]\n'
                      '   ...             )()):\n'
                      '   ...    (my.__dict__.pop(\n'
                      "   ...       '_Qzec6padpw__expr',\n"
                      '   ...       None),\n'
                      '   ...     my.__dict__.pop(\n'
                      "   ...       ('.0'),\n"
                      '   ...       None),\n'
                      '   ...     # QzAT_\n'
                      '   ...     (lambda *xs: [*xs])(\n'
                      '   ...       # zapQzAT_\n'
                      '   ...       # hissp.macros.._macro_.setQzAT_\n'
                      '   ...       # hissp.macros.._macro_.let\n'
                      '   ...       (\n'
                      '   ...        lambda _Qzqfrecvdx__value=iadd(\n'
                      '   ...                 my.a,\n'
                      '   ...                 # hissp.macros.._macro_.setQzAT_\n'
                      '   ...                 # hissp.macros.._macro_.let\n'
                      "   ...                 (lambda _Qzqfrecvdx__value='C':\n"
                      '   ...                    (# hissp.macros.._macro_.define\n'
                      "   ...                     __import__('builtins').setattr(\n"
                      '   ...                       my,\n'
                      "   ...                       'c',\n"
                      '   ...                       _Qzqfrecvdx__value),\n'
                      '   ...                     _Qzqfrecvdx__value)  [-1]\n'
                      '   ...                 )()):\n'
                      '   ...          (# hissp.macros.._macro_.define\n'
                      "   ...           __import__('builtins').setattr(\n"
                      '   ...             my,\n'
                      "   ...             'a',\n"
                      '   ...             _Qzqfrecvdx__value),\n'
                      '   ...           _Qzqfrecvdx__value)  [-1]\n'
                      '   ...       )(),\n'
                      '   ...       my))  [-1]\n'
                      '   ... )()\n'
                      "   ['AC', namespace(a='AC', b='B', c='C')]\n"
                      '\n'
                      'Assignment targets need not be locals, so a scope argument is optional:\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> my## |globals()['spam'], spam.eggs| (|| my#my (list 'abcdefg) ||)\n"
                      '   >>> # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      "   ...  lambda my=__import__('types').SimpleNamespace(\n"
                      '   ...           **# hissp.macros.._macro_.let\n'
                      '   ...             (\n'
                      '   ...              lambda _Qze4jatheu__expr=(\n'
                      '   ...                       # hissp.macros.._macro_.let\n'
                      '   ...                       (lambda '
                      "my=__import__('types').SimpleNamespace(): my)(),\n"
                      '   ...                       list(\n'
                      "   ...                         'abcdefg'),\n"
                      '   ...                       ):\n'
                      "   ...                 [__import__('builtins').locals()\n"
                      "   ...                  for (globals()['spam'], spam.eggs)\n"
                      '   ...                  in [_Qze4jatheu__expr]]  [0]\n'
                      '   ...             )()):\n'
                      '   ...    (my.__dict__.pop(\n'
                      "   ...       '_Qze4jatheu__expr',\n"
                      '   ...       None),\n'
                      '   ...     my.__dict__.pop(\n'
                      "   ...       ('.0'),\n"
                      '   ...       None),\n'
                      '   ...     ())  [-1]\n'
                      '   ... )()\n'
                      '   ()\n'
                      '\n'
                      "   #> my#### spam.eggs[2::2] 'XYZ tomato=spam my ; Assign a global's slice.\n"
                      '   >>> # hissp.macros.._macro_.let\n'
                      '   ... (\n'
                      "   ...  lambda my=__import__('types').SimpleNamespace(\n"
                      '   ...           **# hissp.macros.._macro_.let\n'
                      "   ...             (lambda _Qze4jatheu__expr='XYZ':\n"
                      "   ...                 [__import__('builtins').locals()\n"
                      '   ...                  for (spam.eggs[2::2])\n'
                      '   ...                  in [_Qze4jatheu__expr]]  [0]\n'
                      '   ...             )(),\n'
                      '   ...           tomato=spam):\n'
                      '   ...    (my.__dict__.pop(\n'
                      "   ...       '_Qze4jatheu__expr',\n"
                      '   ...       None),\n'
                      '   ...     my.__dict__.pop(\n'
                      "   ...       ('.0'),\n"
                      '   ...       None),\n'
                      '   ...     my)  [-1]\n'
                      '   ... )()\n'
                      "   namespace(tomato=namespace(eggs=['a', 'b', 'X', 'd', 'Y', 'f', 'Z']))\n"
                      '\n'
                      'See also:\n'
                      '`attach`, `set[### <setQzLSQB_QzHASH_>`, `destruct-> <destructQzH_QzGT_>`.\n'),
             __name__='myQzHASH_',
             __qualname__='_macro_.myQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='myQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'destructQzH_QzGT_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda data, bindings, *body:
              # hissp.macros.._macro_.let
              (
               lambda my=__import__('types').SimpleNamespace(
                        names=list(),
                        QzDOLR_data='_Qzdtesckyo__data'):
                  # progn
                  (# hissp.macros.._macro_.setQzAT_
                   # hissp.macros.._macro_.let
                   (
                    lambda _Qzgx7xjk5f__value=(lambda bindings:
                               # let
                               (
                                lambda pairs=(lambda X:
                                           zip(
                                             X,
                                             X,
                                             strict=True)
                                       )(
                                         iter(
                                           bindings)):
                                   (
                                     '',
                                     ':',
                                     *__import__('itertools').chain.from_iterable(
                                        __import__('itertools').starmap(
                                          (lambda X, Y:
                                              # ifQzH_else
                                              (lambda b, c, a: c()if b else a())(
                                                __import__('hissp').is_node(
                                                  Y),
                                                (lambda :
                                                    (
                                                      ':*',
                                                      (
                                                        'hissp.macros.._macro_.let',
                                                        (
                                                          my.QzDOLR_data,
                                                          (
                                                            'hissp.macros.._macro_.QzH_QzGT_',
                                                            my.QzDOLR_data,
                                                            X,
                                                            ),
                                                          ),
                                                        my.walk(
                                                          Y),
                                                        ),
                                                      )
                                                ),
                                                (lambda :
                                                    # progn
                                                    (my.names.append(
                                                       Y),
                                                     (
                                                       ':?',
                                                       (
                                                         'hissp.macros.._macro_.QzH_QzGT_',
                                                         my.QzDOLR_data,
                                                         X,
                                                         ),
                                                       ))  [-1]
                                                ))
                                          ),
                                          pairs)),
                                     ':?',
                                     '',
                                     )
                               )()
                           ):
                      (# hissp.macros.._macro_.define
                       __import__('builtins').setattr(
                         my,
                         'walk',
                         _Qzgx7xjk5f__value),
                       _Qzgx7xjk5f__value)  [-1]
                   )(),
                   # hissp.macros.._macro_.setQzAT_
                   # hissp.macros.._macro_.let
                   (
                    lambda _Qzgx7xjk5f__value=(
                             'hissp.macros.._macro_.let',
                             (
                               my.QzDOLR_data,
                               data,
                               ),
                             my.walk(
                               bindings),
                             ):
                      (# hissp.macros.._macro_.define
                       __import__('builtins').setattr(
                         my,
                         'values',
                         _Qzgx7xjk5f__value),
                       _Qzgx7xjk5f__value)  [-1]
                   )(),
                   (
                     'hissp.macros.._macro_.letQzH_from',
                     (
                       *my.names,
                       ),
                     my.values,
                     *body,
                     ))  [-1]
              )()
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``destruct->`` 'destruct arrow' Destructuring bindings.\n"
                      '\n'
                      'Bindings are pairs of a transform expression with either a name or\n'
                      '(recursively) another bindings expression. Each transformation\n'
                      'expression is applied to the data via a thread-first\n'
                      '(`-> <QzH_QzGT_>`). This setup allows a bindings form to mirror the\n'
                      "data it's destructuring:\n"
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (% 10 1  'ns (types..SimpleNamespace : a-tuple '(a b c)  spam 'eggs))\n"
                      '   >>> # QzPCENT_\n'
                      '   ... (lambda x0, x1, x2, x3: {x0:x1,x2:x3})(\n'
                      '   ...   (10),\n'
                      '   ...   (1),\n'
                      "   ...   'ns',\n"
                      "   ...   __import__('types').SimpleNamespace(\n"
                      "   ...     aQzH_tuple=('a',\n"
                      "   ...                 'b',\n"
                      "   ...                 'c',),\n"
                      "   ...     spam='eggs'))\n"
                      "   {10: 1, 'ns': namespace(aQzH_tuple=('a', 'b', 'c'), spam='eggs')}\n"
                      '\n'
                      '   #> (define nested-data _)\n'
                      '   >>> # define\n'
                      "   ... __import__('builtins').globals().update(\n"
                      '   ...   nestedQzH_data=_)\n'
                      '\n'
                      '   #> (destruct-> nested-data\n'
                      "   #..            (!#10 num  !#'ns (@#'a-tuple (!#0 a  !#1 b  !#2 c)  "
                      "@#'spam spam))\n"
                      '   #..  (locals))\n'
                      '   >>> # destructQzH_QzGT_\n'
                      '   ... # hissp.macros.._macro_.letQzH_from\n'
                      '   ... (lambda num, a, b, c, spam: locals())(\n'
                      '   ...   *# hissp.macros.._macro_.let\n'
                      '   ...    (lambda _Qzcti67hlh__data=nestedQzH_data:\n'
                      '   ...        (\n'
                      '   ...          # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...          __import__('operator').itemgetter(\n"
                      '   ...            (10))(\n'
                      '   ...            _Qzcti67hlh__data,\n'
                      '   ...            ),\n'
                      '   ...          *# hissp.macros.._macro_.let\n'
                      '   ...           (\n'
                      '   ...            lambda _Qzcti67hlh__data=# '
                      'hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                   __import__('operator').itemgetter(\n"
                      "   ...                     'ns')(\n"
                      '   ...                     _Qzcti67hlh__data,\n'
                      '   ...                     ):\n'
                      '   ...               (\n'
                      '   ...                 *# hissp.macros.._macro_.let\n'
                      '   ...                  (\n'
                      '   ...                   lambda _Qzcti67hlh__data=# '
                      'hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                          __import__('operator').attrgetter(\n"
                      "   ...                            'aQzH_tuple')(\n"
                      '   ...                            _Qzcti67hlh__data,\n'
                      '   ...                            ):\n'
                      '   ...                      (\n'
                      '   ...                        # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                        __import__('operator').itemgetter(\n"
                      '   ...                          (0))(\n'
                      '   ...                          _Qzcti67hlh__data,\n'
                      '   ...                          ),\n'
                      '   ...                        # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                        __import__('operator').itemgetter(\n"
                      '   ...                          (1))(\n'
                      '   ...                          _Qzcti67hlh__data,\n'
                      '   ...                          ),\n'
                      '   ...                        # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                        __import__('operator').itemgetter(\n"
                      '   ...                          (2))(\n'
                      '   ...                          _Qzcti67hlh__data,\n'
                      '   ...                          ),\n'
                      '   ...                        )\n'
                      '   ...                  )(),\n'
                      '   ...                 # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                 __import__('operator').attrgetter(\n"
                      "   ...                   'spam')(\n"
                      '   ...                   _Qzcti67hlh__data,\n'
                      '   ...                   ),\n'
                      '   ...                 )\n'
                      '   ...           )(),\n'
                      '   ...          )\n'
                      '   ...    )())\n'
                      "   {'num': 1, 'a': 'a', 'b': 'b', 'c': 'c', 'spam': 'eggs'}\n"
                      '\n'
                      "But it doesn't have to. Transforms need not be simple lookups:\n"
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (destruct-> nested-data\n'
                      "   #..            (!#'ns (ors ns ; The whole SimpleNamespace (progn works "
                      'too).\n'
                      '   #..                    (getattr \'missing "a default for missing") '
                      'missing\n'
                      "   #..                    @#'spam inner ; attribute lookup\n"
                      "   #..                    @#'a-tuple ([#:-1] ab  [#:] abc ; slices with "
                      'overlaps\n'
                      '   #..                                iter (next A  list rest) ; iterator '
                      'destructuring\n'
                      '   #..                                ;; Composed transform, method calls, '
                      'defaults.\n'
                      '   #..                                (-> enumerate dict) ((.get 2 ()) two\n'
                      '   #..                                                     (.get 3 ()) '
                      'three)\n'
                      '   #..                                ;; Throwaway names must be unique. '
                      '(`$#_ always works).\n'
                      '   #..                                iter (next _0  (next :b) B  next _1  '
                      '(next :d) D)))\n'
                      '   #..             (.get \'quux "default for quux") myquux)\n'
                      '   #..  (pprint..pp (locals)))\n'
                      '   >>> # destructQzH_QzGT_\n'
                      '   ... # hissp.macros.._macro_.letQzH_from\n'
                      '   ... (lambda ns, missing, inner, ab, abc, A, rest, two, three, _0, B, _1, '
                      'D, myquux:\n'
                      "   ...     __import__('pprint').pp(\n"
                      '   ...       locals())\n'
                      '   ... )(\n'
                      '   ...   *# hissp.macros.._macro_.let\n'
                      '   ...    (lambda _Qzcti67hlh__data=nestedQzH_data:\n'
                      '   ...        (\n'
                      '   ...          *# hissp.macros.._macro_.let\n'
                      '   ...           (\n'
                      '   ...            lambda _Qzcti67hlh__data=# '
                      'hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                   __import__('operator').itemgetter(\n"
                      "   ...                     'ns')(\n"
                      '   ...                     _Qzcti67hlh__data,\n'
                      '   ...                     ):\n'
                      '   ...               (\n'
                      '   ...                 # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                 # ors\n'
                      '   ...                 _Qzcti67hlh__data,\n'
                      '   ...                 # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                 getattr(\n'
                      '   ...                   _Qzcti67hlh__data,\n'
                      "   ...                   'missing',\n"
                      "   ...                   ('a default for missing')),\n"
                      '   ...                 # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                 __import__('operator').attrgetter(\n"
                      "   ...                   'spam')(\n"
                      '   ...                   _Qzcti67hlh__data,\n'
                      '   ...                   ),\n'
                      '   ...                 *# hissp.macros.._macro_.let\n'
                      '   ...                  (\n'
                      '   ...                   lambda _Qzcti67hlh__data=# '
                      'hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                          __import__('operator').attrgetter(\n"
                      "   ...                            'aQzH_tuple')(\n"
                      '   ...                            _Qzcti67hlh__data,\n'
                      '   ...                            ):\n'
                      '   ...                      (\n'
                      '   ...                        # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                        (lambda _Qzuah3zizj__items: '
                      '(_Qzuah3zizj__items[:-1]))(\n'
                      '   ...                          _Qzcti67hlh__data,\n'
                      '   ...                          ),\n'
                      '   ...                        # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                        (lambda _Qzuah3zizj__items: '
                      '(_Qzuah3zizj__items[:]))(\n'
                      '   ...                          _Qzcti67hlh__data,\n'
                      '   ...                          ),\n'
                      '   ...                        *# hissp.macros.._macro_.let\n'
                      '   ...                         (\n'
                      '   ...                          lambda _Qzcti67hlh__data=# '
                      'hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                                 iter(\n'
                      '   ...                                   _Qzcti67hlh__data):\n'
                      '   ...                             (\n'
                      '   ...                               # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                               next(\n'
                      '   ...                                 _Qzcti67hlh__data),\n'
                      '   ...                               # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                               list(\n'
                      '   ...                                 _Qzcti67hlh__data),\n'
                      '   ...                               )\n'
                      '   ...                         )(),\n'
                      '   ...                        *# hissp.macros.._macro_.let\n'
                      '   ...                         (\n'
                      '   ...                          lambda _Qzcti67hlh__data=# '
                      'hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                                 # QzH_QzGT_\n'
                      '   ...                                 dict(\n'
                      '   ...                                   enumerate(\n'
                      '   ...                                     _Qzcti67hlh__data)):\n'
                      '   ...                             (\n'
                      '   ...                               # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                               _Qzcti67hlh__data.get(\n'
                      '   ...                                 (2),\n'
                      '   ...                                 ()),\n'
                      '   ...                               # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                               _Qzcti67hlh__data.get(\n'
                      '   ...                                 (3),\n'
                      '   ...                                 ()),\n'
                      '   ...                               )\n'
                      '   ...                         )(),\n'
                      '   ...                        *# hissp.macros.._macro_.let\n'
                      '   ...                         (\n'
                      '   ...                          lambda _Qzcti67hlh__data=# '
                      'hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                                 iter(\n'
                      '   ...                                   _Qzcti67hlh__data):\n'
                      '   ...                             (\n'
                      '   ...                               # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                               next(\n'
                      '   ...                                 _Qzcti67hlh__data),\n'
                      '   ...                               # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                               next(\n'
                      '   ...                                 _Qzcti67hlh__data,\n'
                      "   ...                                 ':b'),\n"
                      '   ...                               # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                               next(\n'
                      '   ...                                 _Qzcti67hlh__data),\n'
                      '   ...                               # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                               next(\n'
                      '   ...                                 _Qzcti67hlh__data,\n'
                      "   ...                                 ':d'),\n"
                      '   ...                               )\n'
                      '   ...                         )(),\n'
                      '   ...                        )\n'
                      '   ...                  )(),\n'
                      '   ...                 )\n'
                      '   ...           )(),\n'
                      '   ...          # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...          _Qzcti67hlh__data.get(\n'
                      "   ...            'quux',\n"
                      "   ...            ('default for quux')),\n"
                      '   ...          )\n'
                      '   ...    )())\n'
                      "   {'ns': namespace(aQzH_tuple=('a', 'b', 'c'), spam='eggs'),\n"
                      "    'missing': 'a default for missing',\n"
                      "    'inner': 'eggs',\n"
                      "    'ab': ('a', 'b'),\n"
                      "    'abc': ('a', 'b', 'c'),\n"
                      "    'A': 'a',\n"
                      "    'rest': ['b', 'c'],\n"
                      "    'two': 'c',\n"
                      "    'three': (),\n"
                      "    '_0': 'a',\n"
                      "    'B': 'b',\n"
                      "    '_1': 'c',\n"
                      "    'D': ':d',\n"
                      "    'myquux': 'default for quux'}\n"
                      '\n'
                      'See also: `let*from <letQzSTAR_from>`, `my# <myQzHASH_>`,\n'
                      '`!s# <QzBANG_sQzHASH_>`, `@s# <QzAT_sQzHASH_>`, `pos# <posQzHASH_>`.\n'),
             __name__='destructQzH_QzGT_',
             __qualname__='_macro_.destructQzH_QzGT_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='destructQzH_QzGT_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzBANG_sQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda names:
              (
                *__import__('itertools').chain.from_iterable(
                   zip(
                     map(
                       (lambda X:
                           (
                             (
                               'operator..itemgetter',
                               (
                                 'quote',
                                 X,
                                 ),
                               ),
                             '',
                             )
                       ),
                       names),
                     names)),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``!s\\#`` 'item names'\n"
                      '\n'
                      '`destruct-> <destructQzH_QzGT_>` helper shorthand.\n'
                      'Destructures a mapping using the binding names as the keys.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (destruct-> (dict : spam 1  foo 2)\n'
                      '   #..            (ors whole\n'
                      '   #..             ors !s#(spam foo))\n'
                      '   #..  (print whole spam foo))\n'
                      '   >>> # destructQzH_QzGT_\n'
                      '   ... # hissp.macros.._macro_.letQzH_from\n'
                      '   ... (lambda whole, spam, foo:\n'
                      '   ...     print(\n'
                      '   ...       whole,\n'
                      '   ...       spam,\n'
                      '   ...       foo)\n'
                      '   ... )(\n'
                      '   ...   *# hissp.macros.._macro_.let\n'
                      '   ...    (\n'
                      '   ...     lambda _Qzxlqqwo2w__data=dict(\n'
                      '   ...              spam=(1),\n'
                      '   ...              foo=(2)):\n'
                      '   ...        (\n'
                      '   ...          # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...          # ors\n'
                      '   ...          _Qzxlqqwo2w__data,\n'
                      '   ...          *# hissp.macros.._macro_.let\n'
                      '   ...           (\n'
                      '   ...            lambda _Qzxlqqwo2w__data=# '
                      'hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                   # ors\n'
                      '   ...                   _Qzxlqqwo2w__data:\n'
                      '   ...               (\n'
                      '   ...                 # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                 __import__('operator').itemgetter(\n"
                      "   ...                   'spam')(\n"
                      '   ...                   _Qzxlqqwo2w__data,\n'
                      '   ...                   ),\n'
                      '   ...                 # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                 __import__('operator').itemgetter(\n"
                      "   ...                   'foo')(\n"
                      '   ...                   _Qzxlqqwo2w__data,\n'
                      '   ...                   ),\n'
                      '   ...                 )\n'
                      '   ...           )(),\n'
                      '   ...          )\n'
                      '   ...    )())\n'
                      "   {'spam': 1, 'foo': 2} 1 2\n"),
             __name__='QzBANG_sQzHASH_',
             __qualname__='_macro_.QzBANG_sQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzBANG_sQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'QzAT_sQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda names:
              (
                *__import__('itertools').chain.from_iterable(
                   zip(
                     map(
                       (lambda X:
                           (
                             (
                               'operator..attrgetter',
                               (
                                 'quote',
                                 X,
                                 ),
                               ),
                             '',
                             )
                       ),
                       names),
                     names)),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``@s\\#`` 'attribute names'\n"
                      '\n'
                      '`destruct-> <destructQzH_QzGT_>` helper shorthand.\n'
                      'Destructures a namespace using the binding names as the attributes.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (destruct-> (types..SimpleNamespace : spam 1  foo 2)\n'
                      '   #..            (ors whole\n'
                      '   #..             ors @s#(spam foo))\n'
                      '   #..  (print whole spam foo))\n'
                      '   >>> # destructQzH_QzGT_\n'
                      '   ... # hissp.macros.._macro_.letQzH_from\n'
                      '   ... (lambda whole, spam, foo:\n'
                      '   ...     print(\n'
                      '   ...       whole,\n'
                      '   ...       spam,\n'
                      '   ...       foo)\n'
                      '   ... )(\n'
                      '   ...   *# hissp.macros.._macro_.let\n'
                      '   ...    (\n'
                      "   ...     lambda _Qzxlqqwo2w__data=__import__('types').SimpleNamespace(\n"
                      '   ...              spam=(1),\n'
                      '   ...              foo=(2)):\n'
                      '   ...        (\n'
                      '   ...          # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...          # ors\n'
                      '   ...          _Qzxlqqwo2w__data,\n'
                      '   ...          *# hissp.macros.._macro_.let\n'
                      '   ...           (\n'
                      '   ...            lambda _Qzxlqqwo2w__data=# '
                      'hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                   # ors\n'
                      '   ...                   _Qzxlqqwo2w__data:\n'
                      '   ...               (\n'
                      '   ...                 # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                 __import__('operator').attrgetter(\n"
                      "   ...                   'spam')(\n"
                      '   ...                   _Qzxlqqwo2w__data,\n'
                      '   ...                   ),\n'
                      '   ...                 # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                 __import__('operator').attrgetter(\n"
                      "   ...                   'foo')(\n"
                      '   ...                   _Qzxlqqwo2w__data,\n'
                      '   ...                   ),\n'
                      '   ...                 )\n'
                      '   ...           )(),\n'
                      '   ...          )\n'
                      '   ...    )())\n'
                      '   namespace(spam=1, foo=2) 1 2\n'),
             __name__='QzAT_sQzHASH_',
             __qualname__='_macro_.QzAT_sQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='QzAT_sQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'posQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda bindings:
              (
                *__import__('itertools').chain.from_iterable(
                   zip(
                     map(
                       (lambda X:
                           (
                             (
                               'operator..itemgetter',
                               X,
                               ),
                             '',
                             )
                       ),
                       # QzH_QzGT_
                       range(
                         len(
                           bindings))),
                     bindings)),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``pos\\#`` 'position bindings'\n"
                      '\n'
                      '`destruct-> <destructQzH_QzGT_>` helper shorthand.\n'
                      "Destructures a sequence using each binding form's position index.\n"
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (destruct-> '(ABC XYZ)\n"
                      '   #..            (ors whole  ors pos#(abc pos#(x y)))\n'
                      '   #..  (print whole abc x y))\n'
                      '   >>> # destructQzH_QzGT_\n'
                      '   ... # hissp.macros.._macro_.letQzH_from\n'
                      '   ... (lambda whole, abc, x, y:\n'
                      '   ...     print(\n'
                      '   ...       whole,\n'
                      '   ...       abc,\n'
                      '   ...       x,\n'
                      '   ...       y)\n'
                      '   ... )(\n'
                      '   ...   *# hissp.macros.._macro_.let\n'
                      '   ...    (\n'
                      "   ...     lambda _Qzzqguiyyn__data=('ABC',\n"
                      "   ...             'XYZ',):\n"
                      '   ...        (\n'
                      '   ...          # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...          # ors\n'
                      '   ...          _Qzzqguiyyn__data,\n'
                      '   ...          *# hissp.macros.._macro_.let\n'
                      '   ...           (\n'
                      '   ...            lambda _Qzzqguiyyn__data=# '
                      'hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...                   # ors\n'
                      '   ...                   _Qzzqguiyyn__data:\n'
                      '   ...               (\n'
                      '   ...                 # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                 __import__('operator').itemgetter(\n"
                      '   ...                   (0))(\n'
                      '   ...                   _Qzzqguiyyn__data,\n'
                      '   ...                   ),\n'
                      '   ...                 *# hissp.macros.._macro_.let\n'
                      '   ...                  (\n'
                      '   ...                   lambda _Qzzqguiyyn__data=# '
                      'hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                          __import__('operator').itemgetter(\n"
                      '   ...                            (1))(\n'
                      '   ...                            _Qzzqguiyyn__data,\n'
                      '   ...                            ):\n'
                      '   ...                      (\n'
                      '   ...                        # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                        __import__('operator').itemgetter(\n"
                      '   ...                          (0))(\n'
                      '   ...                          _Qzzqguiyyn__data,\n'
                      '   ...                          ),\n'
                      '   ...                        # hissp.macros.._macro_.QzH_QzGT_\n'
                      "   ...                        __import__('operator').itemgetter(\n"
                      '   ...                          (1))(\n'
                      '   ...                          _Qzzqguiyyn__data,\n'
                      '   ...                          ),\n'
                      '   ...                        )\n'
                      '   ...                  )(),\n'
                      '   ...                 )\n'
                      '   ...           )(),\n'
                      '   ...          )\n'
                      '   ...    )())\n'
                      "   ('ABC', 'XYZ') ABC X Y\n"),
             __name__='posQzHASH_',
             __qualname__='_macro_.posQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='posQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'case',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda key, default, *pairs:
             (# when
              (lambda b, c: c()if b else())(
                __import__('operator').mod(
                  len(
                    pairs),
                  (2)),
                (lambda :
                    # throw
                    # hissp.macros.._macro_.throwQzSTAR_
                    (lambda g:g.close()or g.throw)(c for c in'')(
                      TypeError(
                        ('incomplete pair')))
                )),
              # let
              (
               lambda kss=(lambda _Qzud7xb74e__items: (_Qzud7xb74e__items[-2::-2]))(
                        pairs),
                      ts=(lambda _Qzud7xb74e__items: (_Qzud7xb74e__items[::-2]))(
                        pairs):
                  (
                    (
                      '.__getitem__',
                      (
                        '',
                        *map(
                           (lambda X:
                               (
                                 'lambda',
                                 ':',
                                 X,
                                 )
                           ),
                           ts),
                        (
                          'lambda',
                          ':',
                          default,
                          ),
                        '',
                        ),
                      (
                        '.get',
                        dict(
                          __import__('itertools').chain.from_iterable(
                            __import__('itertools').starmap(
                              (lambda i, ks:
                                  map(
                                    (lambda X:
                                        # QzAT_
                                        (lambda *xs: [*xs])(
                                          X,
                                          i)
                                    ),
                                    ks)
                              ),
                              enumerate(
                                kss)))),
                        key,
                        (-1),
                        ),
                      ),
                    )
              )())  [-1]
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Switch case macro.\n'
                      '\n'
                      'Precomputes a lookup table (dict), so must switch on a hashable key.\n'
                      "Target keys are not evaluated, so don't quote them; they must be known\n"
                      'at compile time.\n'
                      '\n'
                      'The default case is first and required.\n'
                      'The remainder are implicitly paired by position.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      "   #> (any-map x '(1 2 spam |42| :eggs)\n"
                      '   #..  (case x (print "default")\n'
                      '   #..    (0 2 |42|) (print "even")\n'
                      '   #..    (1 3 spam) (print "odd")))\n'
                      '   >>> # anyQzH_map\n'
                      "   ... __import__('builtins').any(\n"
                      "   ...   __import__('builtins').map(\n"
                      '   ...     (lambda x:\n'
                      '   ...         # case\n'
                      '   ...         (\n'
                      '   ...           (lambda :\n'
                      '   ...               print(\n'
                      "   ...                 ('odd'))\n"
                      '   ...           ),\n'
                      '   ...           (lambda :\n'
                      '   ...               print(\n'
                      "   ...                 ('even'))\n"
                      '   ...           ),\n'
                      '   ...           (lambda :\n'
                      '   ...               print(\n'
                      "   ...                 ('default'))\n"
                      '   ...           ),\n'
                      '   ...           ).__getitem__(\n'
                      "   ...           {1: 0, 3: 0, 'spam': 0, 0: 1, 2: 1, '42': 1}.get(\n"
                      '   ...             x,\n'
                      '   ...             (-1)))()\n'
                      '   ...     ),\n'
                      '   ...     ((1),\n'
                      '   ...      (2),\n'
                      "   ...      'spam',\n"
                      "   ...      '42',\n"
                      "   ...      ':eggs',)))\n"
                      '   odd\n'
                      '   even\n'
                      '   odd\n'
                      '   even\n'
                      '   default\n'
                      '   False\n'
                      '\n'
                      'See also: `cond`.\n'),
             __name__='case',
             __qualname__='_macro_.case',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='case')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'nilQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda x:
              (
                'hissp.macros.._macro_.ors',
                x,
                (),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=("``nil#`` evaluates as ``x or ()``. Adapter for 'nil punning'."),
             __name__='nilQzHASH_',
             __qualname__='_macro_.nilQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='nilQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  '_spy',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr, file:
              (
                'hissp.macros.._macro_.let',
                (
                  '_Qz54qpytal__e',
                  expr,
                  ),
                (
                  'builtins..print',
                  (
                    'pprint..pformat',
                    (
                      'quote',
                      expr,
                      ),
                    ':',
                    'hissp.macros..sort_dicts',
                    (0),
                    ),
                  "('=>')",
                  (
                    'builtins..repr',
                    '_Qz54qpytal__e',
                    ),
                  ':',
                  'hissp.macros..file',
                  file,
                  ),
                '_Qz54qpytal__e',
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __name__='_spy',
             __qualname__='_macro_._spy',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='_spy')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'spyQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(
           lambda expr,
                  file='sys..stderr':
              (
                'hissp.._macro_._spy',
                expr,
                file,
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``spy#`` Print ``expr`` ``=>`` its value, to the file. Return the value.\n'
                      '\n'
                      'Typically used to debug a Lissp expression.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (op#add 5 spy##file=sys..stdout(op#mul 7 3))\n'
                      "   >>> __import__('operator').add(\n"
                      '   ...   (5),\n'
                      '   ...   # hissp.._macro_._spy\n'
                      '   ...   # hissp.macros.._macro_.let\n'
                      '   ...   (\n'
                      "   ...    lambda _Qz764kzbp5__e=__import__('operator').mul(\n"
                      '   ...             (7),\n'
                      '   ...             (3)):\n'
                      "   ...      (__import__('builtins').print(\n"
                      "   ...         __import__('pprint').pformat(\n"
                      "   ...           ('operator..mul',\n"
                      '   ...            (7),\n'
                      '   ...            (3),),\n'
                      '   ...           sort_dicts=(0)),\n'
                      "   ...         ('=>'),\n"
                      "   ...         __import__('builtins').repr(\n"
                      '   ...           _Qz764kzbp5__e),\n'
                      "   ...         file=__import__('sys').stdout),\n"
                      '   ...       _Qz764kzbp5__e)  [-1]\n'
                      '   ...   )())\n'
                      "   ('operator..mul', 7, 3) => 21\n"
                      '   26\n'
                      '\n'
                      'See also: `print`, `doto`, `progn`.\n'),
             __name__='spyQzHASH_',
             __qualname__='_macro_.spyQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='spyQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'timeQzHASH_',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(
           lambda expr,
                  file='sys..stderr':
              (
                'hissp.macros.._macro_.let',
                (
                  '_Qzqbnil4kd__time',
                  'time..time_ns',
                  ),
                (
                  'hissp.macros.._macro_.letQzH_from',
                  (
                    '_Qzqbnil4kd__start',
                    '_Qzqbnil4kd__val',
                    '_Qzqbnil4kd__end',
                    ),
                  (
                    '',
                    (
                      '_Qzqbnil4kd__time',
                      ),
                    expr,
                    (
                      '_Qzqbnil4kd__time',
                      ),
                    ),
                  (
                    'builtins..print',
                    "('time# ran')",
                    (
                      'pprint..pformat',
                      (
                        'quote',
                        expr,
                        ),
                      ':',
                      'hissp.macros..sort_dicts',
                      (0),
                      ),
                    "('in')",
                    (
                      'operator..truediv',
                      (
                        'operator..sub',
                        '_Qzqbnil4kd__end',
                        '_Qzqbnil4kd__start',
                        ),
                      # Decimal('1E+6')
                      __import__('pickle').loads(b'cdecimal\nDecimal\n(V1E+6\ntR.'),
                      ),
                    "('ms')",
                    ':',
                    'hissp.macros..file',
                    file,
                    ),
                  '_Qzqbnil4kd__val',
                  ),
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('``time#`` Print ms elapsed running ``expr`` to the file. Return its value.\n'
                      '\n'
                      'Typically used when optimizing a Lissp expression.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> time##file=sys..stdout(time..sleep .05)\n'
                      '   >>> # hissp.macros.._macro_.let\n'
                      "   ... (lambda _Qz2dtk7y5j__time=__import__('time').time_ns:\n"
                      '   ...     # hissp.macros.._macro_.letQzH_from\n'
                      '   ...     (lambda _Qz2dtk7y5j__start, _Qz2dtk7y5j__val, _Qz2dtk7y5j__end:\n'
                      "   ...        (__import__('builtins').print(\n"
                      "   ...           ('time# ran'),\n"
                      "   ...           __import__('pprint').pformat(\n"
                      "   ...             ('time..sleep',\n"
                      '   ...              (0.05),),\n'
                      '   ...             sort_dicts=(0)),\n'
                      "   ...           ('in'),\n"
                      "   ...           __import__('operator').truediv(\n"
                      "   ...             __import__('operator').sub(\n"
                      '   ...               _Qz2dtk7y5j__end,\n'
                      '   ...               _Qz2dtk7y5j__start),\n'
                      "   ...             # Decimal('1E+6')\n"
                      '   ...             '
                      "__import__('pickle').loads(b'cdecimal\\nDecimal\\n(V1E+6\\ntR.')),\n"
                      "   ...           ('ms'),\n"
                      "   ...           file=__import__('sys').stdout),\n"
                      '   ...         _Qz2dtk7y5j__val)  [-1]\n'
                      '   ...     )(\n'
                      '   ...       *(\n'
                      '   ...          _Qz2dtk7y5j__time(),\n'
                      "   ...          __import__('time').sleep(\n"
                      '   ...            (0.05)),\n'
                      '   ...          _Qz2dtk7y5j__time()))\n'
                      '   ... )()\n'
                      "   time# ran ('time..sleep', 0.05) in ... ms\n"
                      '\n'
                      'See also: `timeit`.\n'),
             __name__='timeQzHASH_',
             __qualname__='_macro_.timeQzHASH_',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='timeQzHASH_')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'avow',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr, predicate, *args:
              (
                'hissp.macros.._macro_.let',
                (
                  'it',
                  expr,
                  ),
                (
                  'hissp.macros.._macro_.unless',
                  (
                    'hissp.macros.._macro_.QzH_QzGT_',
                    'it',
                    predicate,
                    ),
                  (
                    'hissp.macros.._macro_.throw',
                    (
                      'builtins..AssertionError',
                      *args,
                      ),
                    ),
                  ),
                'it',
                )
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Anaphoric. Raises `AssertionError` `unless` ``(-> expr predicate)``.\n'
                      '\n'
                      'Additional arguments are evaluated in a context where ``it`` refers\n'
                      'to the result of ``expr``. These (if any) are passed to the\n'
                      '`AssertionError`. Evaluates to the result of ``expr``.\n'
                      '\n'
                      'Assertions document assumptions that should never be false; only\n'
                      'raise `AssertionError`\\ s to fail fast when there is a bug in your\n'
                      'code violating one, which can never happen if the code was written\n'
                      'correctly. Though implemented as exceptions in Python, they should\n'
                      'almost never be caught, except (perhaps) by a supervising system\n'
                      '(such as a `REPL`) capable of dealing with broken subsystems. They\n'
                      'are not to be used like normal exceptions to handle expected cases.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (avow 7 (X#|X%2 == 0|)\n'
                      '   #..  it "That\'s odd.")\n'
                      '   >>> # avow\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      '   ... (lambda it=(7):\n'
                      '   ...    (# hissp.macros.._macro_.unless\n'
                      '   ...     (lambda b, a: ()if b else a())(\n'
                      '   ...       # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...       (lambda X: X%2 == 0)(\n'
                      '   ...         it),\n'
                      '   ...       (lambda :\n'
                      '   ...           # hissp.macros.._macro_.throw\n'
                      '   ...           # hissp.macros.._macro_.throwQzSTAR_\n'
                      "   ...           (lambda g:g.close()or g.throw)(c for c in'')(\n"
                      "   ...             __import__('builtins').AssertionError(\n"
                      '   ...               it,\n'
                      '   ...               ("That\'s odd.")))\n'
                      '   ...       )),\n'
                      '   ...     it)  [-1]\n'
                      '   ... )()\n'
                      '   Traceback (most recent call last):\n'
                      '     ...\n'
                      '   AssertionError: (7, "That\'s odd.")\n'
                      '\n'
                      'See also: `assert`, `assure`, `throw`.\n'),
             __name__='avow',
             __qualname__='_macro_.avow',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='avow')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())

# defmacro
__import__('builtins').setattr(
  __import__('builtins').globals().get(
    ('_macro_')),
  'assure',
  # hissp.macros.._macro_.fun
  # hissp.macros.._macro_.let
  (
   lambda _Qzwfz72h4o__lambda=(lambda expr, predicate, *args:
              # ifQzH_else
              (lambda b, c, a: c()if b else a())(
                __debug__,
                (lambda :
                    (
                      'hissp.macros.._macro_.avow',
                      expr,
                      predicate,
                      *args,
                      )
                ),
                (lambda : expr))
          ):
     ((
        *__import__('itertools').starmap(
           _Qzwfz72h4o__lambda.__setattr__,
           __import__('builtins').dict(
             __doc__=('Anaphoric. Raises `AssertionError` `unless` ``(-> expr predicate)``.\n'
                      '\n'
                      'As `avow`, but expansion is simply ``expr`` when `__debug__` is off:\n'
                      '\n'
                      '.. code-block:: console\n'
                      '\n'
                      '    $ python -Om hissp -c "(print (assure 0 bool))"\n'
                      '    0\n'
                      '\n'
                      '    $ lissp -c "(print (assure 0 bool))"\n'
                      '    Hissp abort!\n'
                      '    Traceback (most recent call last):\n'
                      '      ...\n'
                      '    AssertionError\n'
                      '\n'
                      "Note that for pre-compiled code, it's the `__debug__` state at\n"
                      'compile time, not at run time, that determines if assure\n'
                      'assertions are turned on.\n'
                      '\n'
                      'For internal integrity checks, prefer `avow` to `assure`, unless\n'
                      'profiling indicates the check is unacceptably expensive in\n'
                      'production, and the risk of not checking is acceptable; assume\n'
                      '`__debug__` will later be turned off.\n'
                      '\n'
                      'Also useful at the top level for quick unit tests in smaller\n'
                      'projects, because they can be turned off. Larger projects may be\n'
                      'better off with `unittest` and separated test modules, which need\n'
                      'not be distributed and likely produce better error messages.\n'
                      '\n'
                      '.. code-block:: REPL\n'
                      '\n'
                      '   #> (assure 7 (X#|X%2 == 0|)\n'
                      '   #..  it "That\'s odd.")\n'
                      '   >>> # assure\n'
                      '   ... # hissp.macros.._macro_.avow\n'
                      '   ... # hissp.macros.._macro_.let\n'
                      '   ... (lambda it=(7):\n'
                      '   ...    (# hissp.macros.._macro_.unless\n'
                      '   ...     (lambda b, a: ()if b else a())(\n'
                      '   ...       # hissp.macros.._macro_.QzH_QzGT_\n'
                      '   ...       (lambda X: X%2 == 0)(\n'
                      '   ...         it),\n'
                      '   ...       (lambda :\n'
                      '   ...           # hissp.macros.._macro_.throw\n'
                      '   ...           # hissp.macros.._macro_.throwQzSTAR_\n'
                      "   ...           (lambda g:g.close()or g.throw)(c for c in'')(\n"
                      "   ...             __import__('builtins').AssertionError(\n"
                      '   ...               it,\n'
                      '   ...               ("That\'s odd.")))\n'
                      '   ...       )),\n'
                      '   ...     it)  [-1]\n'
                      '   ... )()\n'
                      '   Traceback (most recent call last):\n'
                      '     ...\n'
                      '   AssertionError: (7, "That\'s odd.")\n'
                      '\n'
                      'See also: `assert`.\n'),
             __name__='assure',
             __qualname__='_macro_.assure',
             __code__=_Qzwfz72h4o__lambda.__code__.replace(
                        co_name='assure')).items()),
        ),
      _Qzwfz72h4o__lambda)  [-1]
  )())