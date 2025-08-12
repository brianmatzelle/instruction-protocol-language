Hi! This is a natural-language based intruction protocol/ruleset (i.e., compiler) for MCP programs.

Think of this instruction set as a compiler in the form of a monorepo -- a definition for our programming language (called instruction protocol), in which the syntax will be defined not by parsers, asts, etc., but instead by natural language.

This language intends to act as an abstraction for the sequential execution of MCP functions. The language will be self-hosted, in that it will be defined and modified at runtime, with the complete instruction protocol being store on disk so it can be iterated on.

Follow the core Unix principles when defining various rules in this compiler, from syntax to methods/preferred orders of execution.

Core concepts:
Files that start with _ are 'private' or 'meta', i.e. 'offline' context for you when you're developing/iterating on the compiler, not to be used at runtime. This can be anything you'd need for development of the compiler, from next compiler development tasks to meta definitions like how folder structure/modules are linked together.

As the language becomes increasingly defined and turing complete, start writing the compiler in the lanuage itself. Slowly, private files (the ones that start with _) should begin incorporating this language's syntax, until eventually, the entire compiler is written in this language. For example, _TO-BE-DEFINED.un outlines next steps that you should take for the compiler's internal development, outlining architectural questions that have yet to be answered, all of which intend to guide internal development of the compiler. _TO-BE-DEFINED.un is intended to be updated frequently, as internal development of the compiler continues. Furthermore, _RULES.un is intended to contain rules for you to follow at runtime. The workflow is: Execute the script -> if you get stuck, add questions to the _TO-BE-DEFINED.un file, who's solutions would work towards reaching the goal -> think of solutions, come up with new rules scoped to the directory, append that directory's _RULES.un -> continue execution

Actually, I am naming this language: undefined.