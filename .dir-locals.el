;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((python-mode . ((flycheck-flake8rc . ".flake8")
                 (eval . (flycheck-mode t))
                 (eval . (progn
                           (pipenv-activate)))
                 (flycheck--automatically-enabled-checkers . (python-flake8))
                 (flycheck--automatically-disabled-checkers . (python-mypy)))))
