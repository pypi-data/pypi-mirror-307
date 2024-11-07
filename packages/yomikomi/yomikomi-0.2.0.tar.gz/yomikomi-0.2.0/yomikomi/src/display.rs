/// Pretty printing of arrays
/// This implementation should be in line with the PyTorch version.
/// https://github.com/pytorch/pytorch/blob/7b419e8513a024e172eae767e24ec1b849976b13/torch/_tensor_str.py
use crate::{Array, DType, Result, WithDType};

impl Array {
    fn fmt_dt<T: WithDType + std::fmt::Display>(
        &self,
        f: &mut std::fmt::Formatter,
    ) -> std::fmt::Result {
        write!(f, "Array[")?;
        match self.dims() {
            [] => {
                if let Ok(v) = self.to_vec0::<T>() {
                    write!(f, "{v}")?
                }
            }
            [s] if *s < 10 => {
                if let Ok(vs) = self.to_vec1::<T>() {
                    for (i, v) in vs.iter().enumerate() {
                        if i > 0 {
                            write!(f, ", ")?;
                        }
                        write!(f, "{v}")?;
                    }
                }
            }
            dims => {
                write!(f, "dims ")?;
                for (i, d) in dims.iter().enumerate() {
                    if i > 0 {
                        write!(f, ", ")?;
                    }
                    write!(f, "{d}")?;
                }
            }
        }
        write!(f, "; {}]", self.dtype().as_str())
    }
}

impl std::fmt::Debug for Array {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self.dtype() {
            DType::U8 => self.fmt_dt::<u8>(f),
            DType::I8 => self.fmt_dt::<i8>(f),
            DType::U32 => self.fmt_dt::<u32>(f),
            DType::I64 => self.fmt_dt::<i64>(f),
            DType::F32 => self.fmt_dt::<f32>(f),
            DType::F64 => self.fmt_dt::<f64>(f),
        }
    }
}

/// Options for Array pretty printing
pub struct PrinterOptions {
    precision: usize,
    threshold: usize,
    edge_items: usize,
    line_width: usize,
    sci_mode: Option<bool>,
}

static PRINT_OPTS: std::sync::Mutex<PrinterOptions> =
    std::sync::Mutex::new(PrinterOptions::const_default());

impl PrinterOptions {
    // We cannot use the default trait as it's not const.
    const fn const_default() -> Self {
        Self { precision: 4, threshold: 1000, edge_items: 3, line_width: 80, sci_mode: None }
    }
}

pub fn set_print_options(options: PrinterOptions) {
    *PRINT_OPTS.lock().unwrap() = options
}

pub fn set_print_options_default() {
    *PRINT_OPTS.lock().unwrap() = PrinterOptions::const_default()
}

pub fn set_print_options_short() {
    *PRINT_OPTS.lock().unwrap() = PrinterOptions {
        precision: 2,
        threshold: 1000,
        edge_items: 2,
        line_width: 80,
        sci_mode: None,
    }
}

pub fn set_print_options_full() {
    *PRINT_OPTS.lock().unwrap() = PrinterOptions {
        precision: 4,
        threshold: usize::MAX,
        edge_items: 3,
        line_width: 80,
        sci_mode: None,
    }
}

struct FmtSize {
    current_size: usize,
}

impl FmtSize {
    fn new() -> Self {
        Self { current_size: 0 }
    }

    fn final_size(self) -> usize {
        self.current_size
    }
}

impl std::fmt::Write for FmtSize {
    fn write_str(&mut self, s: &str) -> std::fmt::Result {
        self.current_size += s.len();
        Ok(())
    }
}

trait ArrayFormatter {
    type Elem: WithDType;

    fn fmt<T: std::fmt::Write>(&self, v: Self::Elem, max_w: usize, f: &mut T) -> std::fmt::Result;

    fn max_width(&self, to_display: &Array) -> usize {
        let mut max_width = 1;
        if let Ok(vs) = to_display.flatten_all().and_then(|t| t.to_vec1()) {
            for &v in vs.iter() {
                let mut fmt_size = FmtSize::new();
                let _res = self.fmt(v, 1, &mut fmt_size);
                max_width = usize::max(max_width, fmt_size.final_size())
            }
        }
        max_width
    }

    fn write_newline_indent(i: usize, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        writeln!(f)?;
        for _ in 0..i {
            write!(f, " ")?
        }
        Ok(())
    }

    fn fmt_array(
        &self,
        t: &Array,
        indent: usize,
        max_w: usize,
        summarize: bool,
        po: &PrinterOptions,
        f: &mut std::fmt::Formatter,
    ) -> std::fmt::Result {
        let dims = t.dims();
        let edge_items = po.edge_items;
        write!(f, "[")?;
        match dims {
            [] => {
                if let Ok(v) = t.to_vec0::<Self::Elem>() {
                    self.fmt(v, max_w, f)?
                }
            }
            [v] if summarize && *v > 2 * edge_items => {
                if let Ok(vs) = t.narrow(0, 0, edge_items).and_then(|t| t.to_vec1::<Self::Elem>()) {
                    for v in vs.into_iter() {
                        self.fmt(v, max_w, f)?;
                        write!(f, ", ")?;
                    }
                }
                write!(f, "...")?;
                if let Ok(vs) =
                    t.narrow(0, v - edge_items, edge_items).and_then(|t| t.to_vec1::<Self::Elem>())
                {
                    for v in vs.into_iter() {
                        write!(f, ", ")?;
                        self.fmt(v, max_w, f)?;
                    }
                }
            }
            [_] => {
                let elements_per_line = usize::max(1, po.line_width / (max_w + 2));
                if let Ok(vs) = t.to_vec1::<Self::Elem>() {
                    for (i, v) in vs.into_iter().enumerate() {
                        if i > 0 {
                            if i % elements_per_line == 0 {
                                write!(f, ",")?;
                                Self::write_newline_indent(indent, f)?
                            } else {
                                write!(f, ", ")?;
                            }
                        }
                        self.fmt(v, max_w, f)?
                    }
                }
            }
            _ => {
                if summarize && dims[0] > 2 * edge_items {
                    for i in 0..edge_items {
                        match t.get(i) {
                            Ok(t) => self.fmt_array(&t, indent + 1, max_w, summarize, po, f)?,
                            Err(e) => write!(f, "{e:?}")?,
                        }
                        write!(f, ",")?;
                        Self::write_newline_indent(indent, f)?
                    }
                    write!(f, "...")?;
                    Self::write_newline_indent(indent, f)?;
                    for i in dims[0] - edge_items..dims[0] {
                        match t.get(i) {
                            Ok(t) => self.fmt_array(&t, indent + 1, max_w, summarize, po, f)?,
                            Err(e) => write!(f, "{e:?}")?,
                        }
                        if i + 1 != dims[0] {
                            write!(f, ",")?;
                            Self::write_newline_indent(indent, f)?
                        }
                    }
                } else {
                    for i in 0..dims[0] {
                        match t.get(i) {
                            Ok(t) => self.fmt_array(&t, indent + 1, max_w, summarize, po, f)?,
                            Err(e) => write!(f, "{e:?}")?,
                        }
                        if i + 1 != dims[0] {
                            write!(f, ",")?;
                            Self::write_newline_indent(indent, f)?
                        }
                    }
                }
            }
        }
        write!(f, "]")?;
        Ok(())
    }
}

struct FloatFormatter<S: WithDType> {
    int_mode: bool,
    sci_mode: bool,
    precision: usize,
    _phantom: std::marker::PhantomData<S>,
}

impl<S> FloatFormatter<S>
where
    S: WithDType + num_traits::Float + std::fmt::Display,
{
    fn new(t: &Array, po: &PrinterOptions) -> Result<Self> {
        let mut int_mode = true;
        let mut sci_mode = false;

        // Rather than containing all values, this should only include
        // values that end up being displayed according to [threshold].
        let values = t
            .flatten_all()?
            .to_vec1()?
            .into_iter()
            .filter(|v: &S| v.is_finite() && !v.is_zero())
            .collect::<Vec<_>>();
        if !values.is_empty() {
            let mut nonzero_finite_min = S::max_value();
            let mut nonzero_finite_max = S::min_value();
            for &v in values.iter() {
                let v = v.abs();
                if v < nonzero_finite_min {
                    nonzero_finite_min = v
                }
                if v > nonzero_finite_max {
                    nonzero_finite_max = v
                }
            }

            for &value in values.iter() {
                if value.ceil() != value {
                    int_mode = false;
                    break;
                }
            }
            if let Some(v1) = S::from(1000.) {
                if let Some(v2) = S::from(1e8) {
                    if let Some(v3) = S::from(1e-4) {
                        sci_mode = nonzero_finite_max / nonzero_finite_min > v1
                            || nonzero_finite_max > v2
                            || nonzero_finite_min < v3
                    }
                }
            }
        }

        match po.sci_mode {
            None => {}
            Some(v) => sci_mode = v,
        }
        Ok(Self { int_mode, sci_mode, precision: po.precision, _phantom: std::marker::PhantomData })
    }
}

impl<S> ArrayFormatter for FloatFormatter<S>
where
    S: WithDType + num_traits::Float + std::fmt::Display + std::fmt::LowerExp,
{
    type Elem = S;

    fn fmt<T: std::fmt::Write>(&self, v: Self::Elem, max_w: usize, f: &mut T) -> std::fmt::Result {
        if self.sci_mode {
            write!(f, "{v:width$.prec$e}", v = v, width = max_w, prec = self.precision)
        } else if self.int_mode {
            if v.is_finite() {
                write!(f, "{v:width$.0}.", v = v, width = max_w - 1)
            } else {
                write!(f, "{v:max_w$.0}")
            }
        } else {
            write!(f, "{v:width$.prec$}", v = v, width = max_w, prec = self.precision)
        }
    }
}

struct IntFormatter<S: WithDType> {
    _phantom: std::marker::PhantomData<S>,
}

impl<S: WithDType> IntFormatter<S> {
    fn new() -> Self {
        Self { _phantom: std::marker::PhantomData }
    }
}

impl<S> ArrayFormatter for IntFormatter<S>
where
    S: WithDType + std::fmt::Display,
{
    type Elem = S;

    fn fmt<T: std::fmt::Write>(&self, v: Self::Elem, max_w: usize, f: &mut T) -> std::fmt::Result {
        write!(f, "{v:max_w$}")
    }
}

fn get_summarized_data(t: &Array, edge_items: usize) -> Result<Array> {
    let dims = t.dims();
    if dims.is_empty() {
        Ok(t.clone())
    } else if dims.len() == 1 {
        if dims[0] > 2 * edge_items {
            Array::cat(
                &[t.narrow(0, 0, edge_items)?, t.narrow(0, dims[0] - edge_items, edge_items)?],
                0,
            )
        } else {
            Ok(t.clone())
        }
    } else if dims[0] > 2 * edge_items {
        let mut vs: Vec<_> = (0..edge_items)
            .map(|i| get_summarized_data(&t.get(i)?, edge_items))
            .collect::<Result<Vec<_>>>()?;
        for i in (dims[0] - edge_items)..dims[0] {
            vs.push(get_summarized_data(&t.get(i)?, edge_items)?)
        }
        Array::cat(&vs, 0)
    } else {
        let vs: Vec<_> = (0..dims[0])
            .map(|i| get_summarized_data(&t.get(i)?, edge_items))
            .collect::<Result<Vec<_>>>()?;
        Array::cat(&vs, 0)
    }
}

impl std::fmt::Display for Array {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        let po = PRINT_OPTS.lock().unwrap();
        let summarize = self.elem_count() > po.threshold;
        let to_display = if summarize {
            match get_summarized_data(self, po.edge_items) {
                Ok(v) => v,
                Err(err) => return write!(f, "{err:?}"),
            }
        } else {
            self.clone()
        };
        match self.dtype() {
            DType::U8 => {
                let tf: IntFormatter<u8> = IntFormatter::new();
                let max_w = tf.max_width(&to_display);
                tf.fmt_array(self, 1, max_w, summarize, &po, f)?;
                writeln!(f)?;
            }
            DType::I8 => {
                let tf: IntFormatter<i8> = IntFormatter::new();
                let max_w = tf.max_width(&to_display);
                tf.fmt_array(self, 1, max_w, summarize, &po, f)?;
                writeln!(f)?;
            }
            DType::U32 => {
                let tf: IntFormatter<u32> = IntFormatter::new();
                let max_w = tf.max_width(&to_display);
                tf.fmt_array(self, 1, max_w, summarize, &po, f)?;
                writeln!(f)?;
            }
            DType::I64 => {
                let tf: IntFormatter<i64> = IntFormatter::new();
                let max_w = tf.max_width(&to_display);
                tf.fmt_array(self, 1, max_w, summarize, &po, f)?;
                writeln!(f)?;
            }
            DType::F64 => {
                if let Ok(tf) = FloatFormatter::<f64>::new(&to_display, &po) {
                    let max_w = tf.max_width(&to_display);
                    tf.fmt_array(self, 1, max_w, summarize, &po, f)?;
                    writeln!(f)?;
                }
            }
            DType::F32 => {
                if let Ok(tf) = FloatFormatter::<f32>::new(&to_display, &po) {
                    let max_w = tf.max_width(&to_display);
                    tf.fmt_array(self, 1, max_w, summarize, &po, f)?;
                    writeln!(f)?;
                }
            }
        };

        write!(f, "Array[{:?}, {}]", self.dims(), self.dtype().as_str())
    }
}
