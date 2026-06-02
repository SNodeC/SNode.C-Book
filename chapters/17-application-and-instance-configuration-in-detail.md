## Application and Instance Configuration in Detail
### Why this chapter follows the philosophy chapter

Chapter 16 explained the idea behind SNode.C’s configuration system.

This chapter now becomes more concrete.

If the previous chapter answered the question

> Why is configuration a first-class architectural system in SNode.C?

then this chapter answers the question

> How is that system actually organized when I use it in practice?

That means we now move from philosophy to anatomy.

We will look at the configuration model in three nested levels:

- application configuration,
- instance configuration,
- section configuration.

That three-level structure is one of the reasons the framework stays manageable even when applications become larger or run multiple communication roles in one process.

### The three nested scopes

A practical way to understand SNode.C configuration is to imagine three concentric circles.

#### Application scope

This is the scope of the executable as a whole.

It includes concerns such as:

- configuration file handling,
- writing or showing current configuration,
- daemonization,
- logging,
- help and command-line printing,
- application-wide runtime behavior.

#### Instance scope

This is the scope of one named server or client instance.

It includes concerns such as:

- instance identity,
- enable/disable state,
- instance-specific role behavior,
- the collection of sections that shape that role.

#### Section scope

This is the scope of a specific aspect of one instance.

Examples include:

- `local`
- `remote`
- `connection`
- `socket`
- `server`
- `tls`

This layered structure is not cosmetic. It is the actual practical anatomy of the configuration model.

### Application configuration: the outer operational shell

The README’s current help examples make the application level very clear.

At the application scope, options include things like:

- config-file selection,
- config-file writing,
- killing a daemon,
- showing current configuration,
- printing generated command lines,
- version and help,
- log level,
- verbose level,
- quiet mode,
- log-file path,
- daemonization,
- user and group selection for daemonized runs.

This tells us something important.

Application configuration in SNode.C is not about network addresses directly.

It is about the **operational envelope** in which all configured instances live.

That is exactly the right boundary.

### Why application configuration stays above the instances

It is useful to say this explicitly.

Application-level options should not be confused with instance-level communication behavior.

For example:

- log-file path is an application-level operational concern,
- daemonization is an application-level operational concern,
- config-file reading and writing are application-level operational concerns.

By contrast:

- listening port,
- remote host,
- backlog,
- retry behavior,
- TLS certificates for a particular instance,

are instance-facing or section-facing concerns.

This separation is one of the reasons the framework’s command line remains intelligible.

### Instance configuration: the communication role itself

At the next level down sits the instance.

The current live `ConfigInstance` interface and implementation show that an instance has at least these important configuration-facing ideas:

- an instance name,
- a role (`SERVER` or `CLIENT`),
- an explicit disabled state,
- participation in the subcommand hierarchy,
- integration with config display and command-line generation,
- and destruction hooks.

This already tells us how the framework thinks.

An instance is not a random object with some fields.

It is a **named configurable role** inside the application.

That is why instance configuration sits at the center of the model.

### Named instance identity in practice

The instance name is one of the most important configuration facts in the whole framework.

Why?

Because it is the thing that ties together:

- the C++ object,
- the CLI subcommand path,
- the config-file key prefix,
- the help output,
- the operational identity seen by the user.

Once a reader understands this, named instances stop feeling like syntactic decoration.

They become what they really are:

the main addressing mechanism of the configuration system.

### Disabling an instance is more important than it first looks

The current live implementation of `ConfigInstance` makes one subtle but very practical point visible.

When an instance is disabled, required options are forced to become unrequired for that instance.

This is excellent operational behavior.

It means a disabled instance can remain present in the application and in the configuration model without blocking startup just because some otherwise-required settings are absent.

This matters especially in:

- multi-instance applications,
- deployments where only some carriers are active,
- optional Bluetooth or TLS roles,
- staged rollout scenarios,
- local development where some instances are intentionally inactive.

A weaker framework would make disablement clumsy here. SNode.C treats it as a real configuration state.

### Sections: the most important practical organizing device

If instance identity is the main address of the configuration system, then sections are its main organizing device.

The current README shows this very clearly in help output and config examples.

For a typical server instance, sections can include:

- `local`
- `remote`
- `connection`
- `socket`
- `server`
- `tls`

For a client instance, a similar but role-appropriate set exists.

These sections are one of the best design choices in the framework because they group configuration by behavioral concern rather than by implementation accident.

### `ConfigSection` confirms the section model structurally

The live `ConfigSection` abstraction and its template implementation reinforce this beautifully.

A section is attached to a `ConfigInstance`, derives from the subcommand infrastructure, and constructs its description from the section type’s own name and description metadata.

This means sections are not only documented categories. They are actual structural nodes in the configuration hierarchy.

That is exactly why the help system, CLI nesting, and configuration-file key structure all align so naturally.

### The `local` section

The `local` section is one of the most important sections in the whole system.

It describes the local side of the communication role.

Depending on the family, this may mean:

- host and port,
- path,
- Bluetooth address and channel,
- Bluetooth address and PSM.

For a server instance, the `local` section is especially central because it usually describes the binding side of the server.

For a client instance, it describes the local endpoint if that endpoint should be explicitly shaped instead of left wildcarded.

This is one of the clearest examples of a section organizing real architectural meaning.

### The `remote` section

The `remote` section is the natural complement to `local`.

It describes the peer side of the communication role.

For a client instance, this is often the most visibly important section because it answers the question:

> Where is the peer I want to connect to?

For a server instance, `remote` can still matter in the broader connection model even if it is not always configured as explicitly in the simplest listen scenarios.

This section helps preserve one of the framework’s most important conceptual distinctions:

local side and remote side are not the same thing.

That remains true across all supported lower families.

### The `connection` section

The `connection` section gathers options that shape the behavior of established peer relationships.

From the README’s current examples, this includes things like:

- read timeout,
- write timeout,
- read block size,
- write block size,
- termination timeout.

This is an excellent section boundary.

These settings are not primarily about address identity. They are not primarily about listen/connect activation. They are about the behavior of the connection once it exists.

That makes the section easy to reason about.

### The `socket` section

The `socket` section collects options that shape socket behavior more broadly.

The README examples show options such as:

- reuse-address,
- retry,
- retry-on-fatal,
- retry-timeout,
- retry-tries,
- retry-base,
- retry-jitter,
- retry-limit,
- accept-timeout,
- reuse-port,
- and family-specific additions such as `ipv6-only` where applicable.

This section is one of the clearest demonstrations that SNode.C treats operational behavior seriously.

These are not afterthoughts.

They are configuration-visible properties of the communication role.

### The `server` section

For server instances, the `server` section naturally collects server-role-specific options.

The README examples show values such as:

- backlog,
- accepts-per-tick.

This is exactly the right place for such settings.

They are not generic connection settings. They are not address settings. They are not TLS settings.

They belong to the listening/accepting behavior of the server role itself.

Again, the section boundary reflects real behavioral responsibility.

### The `tls` section

Where TLS is present, the `tls` section provides one of the most important examples of the configuration model’s usefulness.

The README shows that this section can carry settings such as:

- certificate chain,
- certificate key,
- certificate key password,
- CA certificate,
- CA certificate directory,
- cipher list,
- SSL/TLS options,
- initialization and shutdown timeouts,
- SNI-related settings.

This is a particularly strong example because TLS is not a minor tweak. It is a serious connection-layer specialization.

And yet the configuration system still handles it in the same structured section model.

That is architectural consistency at work.

### Section names reflect responsibility, not implementation internals

One of the most elegant things about these sections is that they are named in the language of responsibility.

- `local`
- `remote`
- `connection`
- `socket`
- `server`
- `tls`

These are not low-level implementation-detail names.

They are conceptual names.

That makes the configuration model much easier to teach.

A good technical book should point this out explicitly, because naming is one of the hidden reasons a framework either feels clear or muddy.

### Using configuration through the C++ API in detail

The README already established the broad idea that instances expose configuration through `getConfig()`.

This chapter adds a more practical reading habit.

When using the C++ API directly, think in the same section terms the CLI and config file use.

That means examples naturally take forms such as:

- `getConfig()->Local::...`
- `getConfig()->Remote::...`
- socket-related setters,
- server-related setters,
- TLS-related setters.

This is one of the reasons the current convenience wrappers are so educational: they are often visibly just filling the relevant parts of the same configuration object.

So even in code, the section model still helps you think clearly.

### Using configuration on the command line in detail

At the command-line level, the same hierarchy becomes visible textually.

The README examples show that the user progressively enters:

- the application,
- then the instance name,
- then optionally a section,
- then the options of that section.

This means the command line is not a flat bag of flags.

It is a path through the configuration hierarchy.

That is one of the reasons the CLI is so readable once understood.

### Using configuration files in detail

At the configuration-file level, the same hierarchy becomes visible as dotted keys.

The README examples make this very explicit with keys such as:

- `echo.local.port = 8080`
- `echo.remote.host = "localhost"`
- `echo.remote.port = 8080`

This is one of the most satisfying parts of the framework.

The same hierarchy appears in:

- object structure,
- command-line nesting,
- config-file keys.

That level of consistency is rare, and it is one of the reasons SNode.C is so teachable.

### Required configuration and progressive disclosure

The README’s examples of parameterless `listen()` and `connect()` for named instances show another excellent design feature.

When required configuration is missing, the framework reports the missing structure progressively:

- application requires instance,
- instance requires section,
- section requires option.

This is more than nice error handling.

It is a way of teaching the hierarchy at runtime.

A user who starts with too little configuration is guided toward the correct structure step by step.

That is exactly what a well-designed configuration system should do.

### Application-level persistence versus instance-level persistence

Another helpful detail from the README is the distinction between persistent and non-persistent options.

This becomes especially useful in a detailed chapter because it prevents a common misunderstanding.

Not everything that can be specified on the command line is necessarily something that should be written into the long-term configuration of the application.

SNode.C makes this distinction visible.

That helps the user understand what belongs in the durable description of a communication role and what belongs only to one execution context.

### Default values and commented config output

The README’s generated config output shows another subtle but excellent design choice.

Options that currently have default values — including values configured in code — appear commented in the generated configuration display.

This is a very helpful operational feature.

It lets the user see:

- what the framework knows,
- what the defaults are,
- what has been overridden,
- and what could be persisted explicitly.

That makes configuration files not only editable but educational.

### Multi-instance applications become realistic here

This chapter is also the point where the reader should start seeing how well the configuration model supports multi-instance applications.

Because each instance has:

- its own name,
- its own sections,
- its own disabled state,
- its own role-specific configuration,

one executable can host several communication roles without collapsing into chaos.

This is not a side benefit.

It is one of the major reasons the configuration model is worth studying carefully.

### A practical rule for reading configuration

A good reading habit is this:

When you look at a SNode.C configuration, do not start by scanning values randomly.

Start by asking three questions in order:

1. What are the application-wide operational settings?
2. Which instances exist and which of them are enabled?
3. For each instance, how are its sections shaping the role?

This reading order matches the architecture and prevents confusion.

### Common misunderstandings about application and instance configuration

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Application configuration and instance configuration are basically the same thing.”

Corrected view: application configuration shapes the operational shell of the executable, while instance configuration shapes one concrete communication role.

#### Misunderstanding 2: “Sections are optional organizational sugar.”

Corrected view: sections are structural parts of the configuration model and map directly to behavioral responsibility.

#### Misunderstanding 3: “Disablement is just a Boolean convenience flag.”

Corrected view: disablement is a first-class instance state that meaningfully affects requiredness and multi-instance operation.

#### Misunderstanding 4: “The CLI hierarchy is different from the config-file hierarchy.”

Corrected view: they are two textual views of the same underlying model.

#### Misunderstanding 5: “The detailed config model is only for deployment, not for design.”

Corrected view: the configuration structure reflects the architecture itself and therefore helps with design as well as operation.

### A good one-paragraph summary of the chapter

Application and instance configuration in SNode.C are organized as a nested hierarchy in which the executable defines the operational shell, each named server or client instance becomes a separately configurable communication role, and each role is then shaped through sections such as `local`, `remote`, `connection`, `socket`, `server`, and `tls`. The same hierarchy appears consistently in the C++ API, the command line, and configuration files, which is why the model remains understandable even as applications grow more complex.

That is the heart of the chapter.

### Closing perspective

This chapter has taken the configuration philosophy from Chapter 16 and turned it into a working anatomical map.

The reader should now be able to see configuration not as a list of flags, but as a structured description of:

- the application shell,
- the named communication roles inside it,
- and the behavioral sections that shape those roles.

That is an important milestone.

It means the reader is now prepared to understand operational behavior much more concretely.

And that naturally leads to the next chapter.

Once an application and its instances are configured, the next practical question is:

How do we observe them, diagnose them, and understand what they are doing at runtime?

That means logging, diagnostics, and runtime visibility come next.
