
Manual on ifcopenshell is here
https://docs.ifcopenshell.org/ifcopenshell-python/hello_world.html


# Standard Shape Entities in IFC Files

In IFC files, specific entities are used to represent standard shape profiles. These predefined geometric profiles simplify the modeling of common cross-sections in building elements such as beams, columns, and pipes.

## 1. **IfcRectangleProfileDef**
- **Purpose**: Defines a rectangular profile.
- **Attributes**:
  - `XDim`: Width of the rectangle.
  - `YDim`: Height of the rectangle.
- **Use Case**: Rectangular beams, columns, or slabs.

## 2. **IfcCircleProfileDef**
- **Purpose**: Represents a circular profile.
- **Attributes**:
  - `Radius`: Radius of the circle.
- **Use Case**: Circular columns, pipes, and cylindrical objects.

## 3. **IfcIShapeProfileDef**
- **Purpose**: Describes an I-shaped (or H-shaped) profile.
- **Attributes**:
  - `OverallWidth`: Width of the flange.
  - `OverallDepth`: Height of the profile.
  - `WebThickness`: Thickness of the web.
  - `FlangeThickness`: Thickness of the flanges.
- **Use Case**: Steel beams, girders, and structural members with I-shaped cross-sections.

## 4. **IfcTShapeProfileDef**
- **Purpose**: Defines a T-shaped profile.
- **Attributes**:
  - `OverallWidth`, `OverallDepth`, `WebThickness`, `FlangeThickness`: Similar to `IfcIShapeProfileDef`, but tailored for T-shaped sections.
- **Use Case**: Structural beams and supports with T-shaped cross-sections.

## 5. **IfcLShapeProfileDef**
- **Purpose**: Represents an L-shaped (angle) profile.
- **Attributes**:
  - `OverallWidth`: Width of one leg.
  - `OverallDepth`: Width of the other leg.
  - `Thickness`: Thickness of the profile.
- **Use Case**: Angle sections for supports, trusses, and connections.

## 6. **IfcUShapeProfileDef**
- **Purpose**: Defines a U-shaped (channel) profile.
- **Attributes**:
  - `OverallWidth`, `OverallDepth`, `WebThickness`, `FlangeThickness`.
- **Use Case**: Channels for structural framing, purlins, and beams.

## 7. **IfcCShapeProfileDef**
- **Purpose**: Represents a C-shaped (similar to a channel but with different proportioning) profile.
- **Attributes**:
  - `OverallWidth`, `OverallDepth`, `WebThickness`, `FlangeThickness`.
- **Use Case**: Beams and sections that need a C-shaped profile.

## 8. **IfcZShapeProfileDef**
- **Purpose**: Describes a Z-shaped profile.
- **Attributes**:
  - `OverallWidth`, `OverallDepth`, `WebThickness`, `FlangeThickness`.
- **Use Case**: Structural members and trusses with Z-shaped cross-sections.

## 9. **IfcEllipseProfileDef**
- **Purpose**: Defines an elliptical profile.
- **Attributes**:
  - `SemiAxis1`: Length of the first semi-axis.
  - `SemiAxis2`: Length of the second semi-axis.
- **Use Case**: Decorative columns or features with an elliptical cross-section.

## 10. **IfcTrapeziumProfileDef**
- **Purpose**: Represents a trapezoidal profile.
- **Attributes**:
  - `BottomXDim`, `TopXDim`: Length of the bottom and top sides.
  - `YDim`: Vertical height of the trapezoid.
- **Use Case**: Tapered beams or supports.

## 11. **IfcParameterizedProfileDef**
- **Purpose**: Abstract base class for all parametric (standard) profile definitions. All the above entities inherit from this class.
- **Use Case**: Used as the basis for creating other standard profiles based on predefined parameters.

# Usage in IFC Files
- These profiles are commonly used with entities like `IfcExtrudedAreaSolid` to create 3D elements.
- Standard profile types ensure consistency and simplify data exchange in BIM projects by providing ready-made templates for cross-sections.
